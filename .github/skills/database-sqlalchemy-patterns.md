---
name: database-sqlalchemy-patterns
description: SQLAlchemy ORM patterns and best practices for database operations
technologies: [Python, SQLAlchemy, PostgreSQL]
repositories: [ticketremaster-b, source-repo-code]
---

# SQLAlchemy Database Patterns

## When to Use

Use this skill when creating or modifying database models, queries, or migrations in Python services.

## Prerequisites

- Python 3.12+
- Basic SQL knowledge
- Understanding of ORM concepts

## Step-by-Step Instructions

### 1. Model Definition

```python
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app import db

class User(db.Model):
    __tablename__ = "users"
    
    # Primary key with explicit naming
    id = Column(String(64), primary_key=True)
    
    # Timestamps
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Regular fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    isActive = Column(Boolean, default=True)
    
    # Relationships
    tickets = relationship("Ticket", back_populates="owner", lazy="dynamic")
    
    def to_dict(self, include_sensitive=False):
        """Convert model to dictionary for API responses."""
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "createdAt": self.createdAt.isoformat(),
            "isActive": self.isActive,
        }
        if include_sensitive:
            # Only include sensitive fields when explicitly requested
            pass
        return data
```

### 2. Query Patterns

```python
# Basic queries
def get_user_by_id(user_id: str) -> User | None:
    return db.session.get(User, user_id)

def get_user_by_email(email: str) -> User | None:
    return db.session.query(User).filter(User.email == email).first()

# Paginated queries
def list_users(page: int = 1, per_page: int = 20):
    return User.query.order_by(User.createdAt.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

# Complex queries with joins
def get_users_with_tickets():
    return (
        db.session.query(User, Ticket)
        .join(Ticket, Ticket.ownerId == User.id)
        .filter(User.isActive == True)
        .all()
    )
```

### 3. Transactions and Session Management

```python
from contextlib import contextmanager

@contextmanager
def transaction():
    """Context manager for database transactions."""
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

# Usage
with transaction() as session:
    user = User(id="usr_001", email="test@example.com", name="Test User")
    session.add(user)
    session.flush()  # Get the ID before commit
```

### 4. Bulk Operations

```python
def bulk_insert_users(users_data: list[dict]):
    """Efficiently insert multiple users."""
    users = [User(**data) for data in users_data]
    db.session.bulk_save_objects(users)
    db.session.commit()

def bulk_update_status(user_ids: list[str], is_active: bool):
    """Efficiently update multiple records."""
    User.query.filter(User.id.in_(user_ids)).update(
        {User.isActive: is_active}, synchronize_session=False
    )
    db.session.commit()
```

### 5. Migrations with Alembic

```bash
# Generate migration
alembic revision --autogenerate -m "Add user isActive field"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Common Pitfalls

1. **N+1 queries** - Use `joinedload()` or `selectinload()` for relationships
2. **Forgetting to commit** - Always commit after write operations
3. **Not handling None** - Check for None before accessing attributes
4. **Leaking sessions** - Use context managers or try/finally
5. **Missing indexes** - Add indexes on frequently queried columns

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
