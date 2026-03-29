---
name: microservices-saga-pattern
description: Distributed transaction patterns for microservices - sagas, compensations, and coordination
technologies: [Python, Microservices, RabbitMQ, Distributed Systems]
repositories: [ticketremaster-b, source-repo-code]
---

# Microservices Saga Pattern

## When to Use

Use this skill when implementing multi-step business flows that span multiple microservices in a distributed system.

## Prerequisites

- Understanding of microservices architecture
- Familiarity with REST APIs and message queues
- Basic knowledge of distributed transactions

## Step-by-Step Instructions

### 1. Saga Pattern Overview

A saga is a sequence of local transactions where each transaction updates data within a single service. If a step fails, the saga executes compensating transactions to undo the changes made by preceding steps.

```
Step 1: Hold Seat (Seat Inventory Service)
Step 2: Deduct Credits (Credit Service)
Step 3: Create Ticket (Ticket Service)
Step 4: Log Transaction (Ticket Log Service)

If any step fails:
Compensation: Release Seat → Refund Credits → Delete Ticket
```

### 2. Orchestrator Implementation

```python
# ticket-purchase-orchestrator/orchestrator.py
from typing import List, Dict, Any
from services import SeatInventoryService, CreditService, TicketService, TicketLogService
from compensations import Compensator

class TicketPurchaseSaga:
    def __init__(self):
        self.seat_service = SeatInventoryService()
        self.credit_service = CreditService()
        self.ticket_service = TicketService()
        self.log_service = TicketLogService()
        self.compensator = Compensator()
    
    def execute(self, user_id: str, inventory_id: str, price: float) -> Dict[str, Any]:
        completed_steps: List[str] = []
        step_data: Dict[str, Any] = {}
        
        try:
            # Step 1: Hold seat
            hold_result = self.seat_service.hold_seat(inventory_id, user_id, ttl=300)
            step_data['hold_id'] = hold_result['holdId']
            completed_steps.append('hold_seat')
            
            # Step 2: Deduct credits
            transaction = self.credit_service.deduct_credits(
                user_id, price, reason='ticket_purchase', reference_id=inventory_id
            )
            step_data['transaction_id'] = transaction['txnId']
            completed_steps.append('deduct_credits')
            
            # Step 3: Create ticket
            ticket = self.ticket_service.create_ticket(
                inventory_id=inventory_id,
                owner_id=user_id,
                price=price,
                hold_id=step_data['hold_id']
            )
            step_data['ticket_id'] = ticket['ticketId']
            completed_steps.append('create_ticket')
            
            # Step 4: Log transaction
            self.log_service.log_scan(
                ticket_id=step_data['ticket_id'],
                staff_id=user_id,  # For purchase, user is the staff
                status='purchased'
            )
            completed_steps.append('log_transaction')
            
            return {
                'success': True,
                'ticket_id': step_data['ticket_id'],
                'transaction_id': step_data['transaction_id']
            }
        
        except Exception as e:
            # Execute compensations in reverse order
            self.compensator.compensate(completed_steps, step_data, user_id, inventory_id, price)
            raise
    
    def compensate(self, completed_steps, step_data, user_id, inventory_id, price):
        compensator = Compensator()
        compensator.compensate(completed_steps, step_data, user_id, inventory_id, price)
```

### 3. Compensation Pattern

```python
# ticket-purchase-orchestrator/compensations.py
class Compensator:
    def __init__(self):
        self.seat_service = SeatInventoryService()
        self.credit_service = CreditService()
        self.ticket_service = TicketService()
    
    def compensate(self, completed_steps: List[str], step_data: Dict[str, Any], 
                   user_id: str, inventory_id: str, price: float):
        # Compensate in reverse order
        if 'log_transaction' in completed_steps:
            # Log compensation is just a reverse log entry
            self.log_compensation(step_data['ticket_id'], user_id)
        
        if 'create_ticket' in completed_steps:
            self.ticket_service.cancel_ticket(step_data['ticket_id'])
        
        if 'deduct_credits' in completed_steps:
            self.credit_service.refund_credits(
                user_id, price, reason='purchase_failed', 
                reference_id=step_data['transaction_id']
            )
        
        if 'hold_seat' in completed_steps:
            self.seat_service.release_seat(inventory_id, step_data['hold_id'])
    
    def log_compensation(self, ticket_id: str, user_id: str):
        # Log the compensation for audit purposes
        pass
```

### 4. RabbitMQ Integration for Async Compensation

```python
# ticket-purchase-orchestrator/rabbitmq_handler.py
import pika
import json
from datetime import datetime, timedelta

class RabbitMQHandler:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        
        # Declare TTL queue for seat hold expiry
        self.channel.queue_declare(
            queue='seat_hold_expiry',
            arguments={
                'x-message-ttl': 300000,  # 5 minutes TTL
                'x-dead-letter-exchange': 'seat_hold_dead_letter'
            }
        )
        
        # Declare dead letter queue for expired holds
        self.channel.queue_declare(queue='seat_hold_dead_letter')
        
        # Bind to dead letter exchange
        self.channel.queue_bind(
            queue='seat_hold_dead_letter',
            exchange='seat_hold_dead_letter',
            routing_key='seat_hold_expired'
        )
    
    def publish_hold_message(self, inventory_id: str, hold_id: str):
        message = {
            'inventory_id': inventory_id,
            'hold_id': hold_id,
            'expires_at': (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='seat_hold_expiry',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
    
    def handle_expired_hold(self, method, properties, body):
        message = json.loads(body)
        inventory_id = message['inventory_id']
        hold_id = message['hold_id']
        
        # Release the seat if it's still held
        try:
            self.seat_service.release_seat(inventory_id, hold_id)
        except Exception as e:
            # Log error but don't fail - seat might already be sold
            print(f"Error releasing expired hold: {e}")
        
        # Acknowledge message after processing
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
    
    def start_consuming(self):
        self.channel.basic_consume(
            queue='seat_hold_dead_letter',
            on_message_callback=self.handle_expired_hold
        )
        self.channel.start_consuming()
```

### 5. Service-to-Service Communication

```python
# shared/services.py
import requests
from typing import Dict, Any

class SeatInventoryService:
    def __init__(self):
        self.base_url = "http://seat-inventory-service:5000"
    
    def hold_seat(self, inventory_id: str, user_id: str, ttl: int) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/seats/{inventory_id}/hold",
            json={'userId': user_id, 'ttlSeconds': ttl},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    
    def release_seat(self, inventory_id: str, hold_id: str) -> Dict[str, Any]:
        response = requests.delete(
            f"{self.base_url}/seats/{inventory_id}/hold",
            json={'holdId': hold_id},
            timeout=5
        )
        response.raise_for_status()
        return response.json()

class CreditService:
    def __init__(self):
        self.base_url = "http://credit-transaction-service:5000"
    
    def deduct_credits(self, user_id: str, amount: float, reason: str, reference_id: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/credits/deduct",
            json={
                'userId': user_id,
                'amount': amount,
                'reason': reason,
                'referenceId': reference_id
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    
    def refund_credits(self, user_id: str, amount: float, reason: str, reference_id: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/credits/refund",
            json={
                'userId': user_id,
                'amount': amount,
                'reason': reason,
                'referenceId': reference_id
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
```

## Common Pitfalls

1. **Not implementing compensations** - Every step must have a compensation
2. **Ignoring partial failures** - Handle network timeouts and service unavailability
3. **Race conditions** - Use optimistic locking or version numbers
4. **Not logging compensations** - Always log compensations for audit trails
5. **Missing idempotency** - Ensure compensations are idempotent

## References

- [Microservices Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Distributed Transactions in Microservices](https://www.nginx.com/blog/data-consistency-event-driven-architecture-microservices/)
