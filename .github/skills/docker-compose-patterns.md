---
name: docker-compose-patterns
description: Docker Compose best practices for microservices development and deployment
technologies: [Docker, Docker Compose, Microservices]
repositories: [ticketremaster-b, source-repo-code]
---

# Docker Compose Patterns

## When to Use

Use this skill when creating or modifying Docker Compose configurations for microservices applications.

## Prerequisites

- Basic Docker knowledge
- Understanding of containerization concepts
- Familiarity with networking and volumes

## Step-by-Step Instructions

### 1. Base Dockerfile Pattern

```dockerfile
# services/user-service/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Use gunicorn for production (NOT Flask dev server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. Multi-Service Dockerfile (gRPC + REST)

```dockerfile
# services/seat-inventory-service/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose both REST and gRPC ports
EXPOSE 5000 50051

# Custom entrypoint to start both servers
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
# services/seat-inventory-service/entrypoint.sh
#!/bin/bash

# Start gRPC server in background
python grpc_server.py &

# Start REST API server (foreground)
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-ticketmaster}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-devpassword}
      POSTGRES_DB: ${DB_NAME:-ticketmaster}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-ticketmaster}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3-management-alpine
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-guest}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS:-guest}
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # User Service
  user-service:
    build:
      context: ./services/user-service
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://${DB_USER:-ticketmaster}:${DB_PASSWORD:-devpassword}@postgres:5432/${DB_NAME:-ticketmaster}_user
      REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    ports:
      - "5001:5000"
    volumes:
      - ./services/user-service:/app
    restart: unless-stopped

  # Seat Inventory Service (gRPC + REST)
  seat-inventory-service:
    build:
      context: ./services/seat-inventory-service
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://${DB_USER:-ticketmaster}:${DB_PASSWORD:-devpassword}@postgres:5432/${DB_NAME:-ticketmaster}_seat_inventory
      REDIS_URL: redis://redis:6379/1
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    ports:
      - "5002:5000"   # REST
      - "50051:50051" # gRPC
    volumes:
      - ./services/seat-inventory-service:/app
    restart: unless-stopped

  # API Gateway (Kong)
  kong:
    image: kong:3.4-alpine
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
    ports:
      - "8000:8000"   # Proxy
      - "8001:8001"   # Admin API
      - "8443:8443"   # Proxy SSL
      - "8444:8444"   # Admin API SSL
    volumes:
      - ./kong/declarative:/kong/declarative
    depends_on:
      - user-service
      - seat-inventory-service
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

### 4. Environment Configuration

```bash
# .env
# Database
DB_USER=ticketmaster
DB_PASSWORD=devpassword
DB_NAME=ticketmaster

# Redis
REDIS_URL=redis://redis:6379

# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASS=guest

# API Gateway
KONG_ADMIN_GUI_URL=http://localhost:8001

# Services
JWT_SECRET=your-secret-key-here
ENCRYPTION_KEY=your-32-char-encryption-key
```

### 5. Health Checks

```yaml
# Add to each service
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 6. Development Overrides

```yaml
# docker-compose.override.yml (git-ignored)
version: '3.8'

services:
  user-service:
    build:
      context: ./services/user-service
      dockerfile: Dockerfile
      target: development  # Use development stage if multi-stage
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: 1
    volumes:
      - ./services/user-service:/app
      - /app/__pycache__
    command: flask run --host=0.0.0.0 --port=5000 --reload
```

## Common Pitfalls

1. **Not using healthchecks** - Always add healthchecks for dependencies
2. **Hardcoding ports** - Use environment variables for port mapping
3. **Missing volumes** - Use volumes for data persistence
4. **Not setting restart policies** - Use `restart: unless-stopped`
5. **Ignoring security** - Never use default passwords in production

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/develop-images/multistage-build/)
