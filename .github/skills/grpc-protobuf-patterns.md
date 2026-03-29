---
name: grpc-protobuf-patterns
description: gRPC and Protocol Buffers patterns for microservices communication
technologies: [Python, gRPC, Protocol Buffers]
repositories: [ticketremaster-b, source-repo-code]
---

# gRPC and Protocol Buffers Patterns

## When to Use

Use this skill when creating or modifying gRPC services and Protocol Buffer definitions in Python microservices.

## Prerequisites

- Basic understanding of RPC concepts
- Familiarity with Python packaging
- Understanding of service-oriented architecture

## Step-by-Step Instructions

### 1. Proto File Structure

```protobuf
// proto/seat_inventory.proto
syntax = "proto3";

package seatinventory;

service SeatInventoryService {
  rpc HoldSeat (HoldSeatRequest) returns (HoldSeatResponse);
  rpc ReleaseSeat (ReleaseSeatRequest) returns (ReleaseSeatResponse);
  rpc GetAvailability (AvailabilityRequest) returns (AvailabilityResponse);
}

message HoldSeatRequest {
  string inventoryId = 1;
  string userId = 2;
  int32 ttlSeconds = 3;
}

message HoldSeatResponse {
  bool success = 1;
  string holdId = 2;
  string message = 3;
}

message ReleaseSeatRequest {
  string inventoryId = 1;
  string holdId = 2;
}

message ReleaseSeatResponse {
  bool success = 1;
  string message = 2;
}

message AvailabilityRequest {
  string eventId = 1;
  string venueId = 2;
}

message AvailabilityResponse {
  repeated SeatAvailability seats = 1;
}

message SeatAvailability {
  string inventoryId = 1;
  string seatNumber = 2;
  string rowNumber = 3;
  string status = 4; // available, held, sold
}
```

### 2. Generate Python Stubs

```bash
# Generate Python gRPC code from proto
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./shared/grpc \
  --grpc_python_out=./shared/grpc \
  ./proto/seat_inventory.proto
```

This generates:
- `seat_inventory_pb2.py` - Message classes
- `seat_inventory_pb2_grpc.py` - Service stubs and servicers

### 3. Implement gRPC Server

```python
# seat-inventory-service/grpc_server.py
import grpc
from concurrent import futures
import time

from shared.grpc import seat_inventory_pb2
from shared.grpc import seat_inventory_pb2_grpc
from models import SeatInventory
from app import db

class SeatInventoryServicer(seat_inventory_pb2_grpc.SeatInventoryServiceServicer):
    def HoldSeat(self, request, context):
        inventory = SeatInventory.query.get(request.inventoryId)
        if not inventory:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Seat inventory not found')
            return seat_inventory_pb2.HoldSeatResponse(
                success=False,
                message='Seat not found'
            )
        
        if inventory.status != 'available':
            return seat_inventory_pb2.HoldSeatResponse(
                success=False,
                message='Seat not available'
            )
        
        # Hold the seat
        inventory.status = 'held'
        inventory.heldUntil = time.time() + request.ttlSeconds
        inventory.holdId = f"hold_{int(time.time())}_{request.userId}"
        db.session.commit()
        
        return seat_inventory_pb2.HoldSeatResponse(
            success=True,
            holdId=inventory.holdId,
            message='Seat held successfully'
        )
    
    def ReleaseSeat(self, request, context):
        inventory = SeatInventory.query.get(request.inventoryId)
        if not inventory or inventory.holdId != request.holdId:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Hold not found')
            return seat_inventory_pb2.ReleaseSeatResponse(
                success=False,
                message='Hold not found'
            )
        
        inventory.status = 'available'
        inventory.holdId = None
        inventory.heldUntil = None
        db.session.commit()
        
        return seat_inventory_pb2.ReleaseSeatResponse(
            success=True,
            message='Seat released'
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    seat_inventory_pb2_grpc.add_SeatInventoryServiceServicer_to_server(
        SeatInventoryServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### 4. gRPC Client Usage

```python
# ticket-purchase-orchestrator/seat_client.py
import grpc
from shared.grpc import seat_inventory_pb2
from shared.grpc import seat_inventory_pb2_grpc

class SeatInventoryClient:
    def __init__(self, channel):
        self.stub = seat_inventory_pb2_grpc.SeatInventoryServiceStub(channel)
    
    def hold_seat(self, inventory_id, user_id, ttl_seconds=300):
        request = seat_inventory_pb2.HoldSeatRequest(
            inventoryId=inventory_id,
            userId=user_id,
            ttlSeconds=ttl_seconds
        )
        response = self.stub.HoldSeat(request)
        return response
    
    def release_seat(self, inventory_id, hold_id):
        request = seat_inventory_pb2.ReleaseSeatRequest(
            inventoryId=inventory_id,
            holdId=hold_id
        )
        response = self.stub.ReleaseSeat(request)
        return response

# Usage
channel = grpc.insecure_channel('localhost:50051')
client = SeatInventoryClient(channel)
response = client.hold_seat('inv_001', 'usr_001', 300)
if response.success:
    print(f"Seat held: {response.holdId}")
```

### 5. Docker Compose Configuration

```yaml
# docker-compose.yml
services:
  seat-inventory-service:
    build: ./services/seat-inventory-service
    ports:
      - "5000:5000"   # REST API
      - "50051:50051" # gRPC
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/seat_inventory
    depends_on:
      - postgres

  ticket-purchase-orchestrator:
    build: ./orchestrators/ticket-purchase-orchestrator
    environment:
      - SEAT_INVENTORY_GRPC_URL=seat-inventory-service:50051
    depends_on:
      - seat-inventory-service
```

## Common Pitfalls

1. **Forgetting to regenerate stubs** - Always regenerate after proto changes
2. **Not handling gRPC errors** - Use proper error handling with status codes
3. **Blocking calls** - Use async gRPC for high-concurrency scenarios
4. **Missing deadline** - Always set timeouts on gRPC calls
5. **Not closing channels** - Use context managers for channel lifecycle

## References

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [gRPC Best Practices](https://grpc.io/docs/guides/)
