---
name: python-type-hints
description: Type annotations and mypy best practices for Python code quality
technologies: [Python, Type Hints, mypy]
repositories: [ticketremaster-b, source-repo-code]
---

# Python Type Hints and mypy

## When to Use

Use this skill when writing Python code to ensure type safety and catch errors early through static type checking.

## Prerequisites

- Python 3.12+
- Basic understanding of Python typing module
- Familiarity with mypy for type checking

## Step-by-Step Instructions

### 1. Basic Type Annotations

```python
from typing import List, Dict, Optional, Union
from datetime import datetime

# Simple types
name: str = "Alice"
age: int = 30
is_active: bool = True

# Collections
tags: List[str] = ["python", "typing"]
scores: Dict[str, int] = {"math": 95, "english": 88}

# Optional types
email: Optional[str] = None  # Can be str or None
phone: str | None = None      # Python 3.10+ syntax

# Union types
user_id: Union[str, int] = "usr_001"  # Can be str or int
status: str | int = "active"           # Python 3.10+ syntax
```

### 2. Function Type Annotations

```python
from typing import List, Optional, Tuple

def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting message."""
    return f"{greeting}, {name}!"

def get_user(user_id: str) -> Optional[dict]:
    """Fetch user by ID, returns None if not found."""
    # Implementation
    pass

def process_data(data: List[int]) -> Tuple[int, float]:
    """Process data and return count and average."""
    total = sum(data)
    count = len(data)
    return count, total / count if count > 0 else 0.0
```

### 3. Class Type Annotations

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: str
    email: str
    name: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "isActive": self.is_active,
        }

class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve user by ID."""
        result = self.db.query("SELECT * FROM users WHERE id = %s", (user_id,))
        if result:
            return User(**result)
        return None
    
    def create_user(self, email: str, name: str) -> User:
        """Create new user and return instance."""
        user_id = generate_user_id()
        user = User(id=user_id, email=email, name=name)
        self.db.insert("users", user.to_dict())
        return user
```

### 4. Type Aliases and NewType

```python
from typing import NewType, List

# Type alias for clarity
UserId = str
EventId = str
SeatNumber = str

# NewType for stronger type checking
UserId = NewType("UserId", str)
EventId = NewType("EventId", str)

def get_user(user_id: UserId) -> User:
    # Implementation
    pass

# Usage
user_id = UserId("usr_001")  # Explicit conversion
event_id = EventId("evt_001")
```

### 5. Generics

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, entity_type: type[T]):
        self.entity_type = entity_type
    
    def get_by_id(self, entity_id: str) -> T | None:
        # Implementation
        pass
    
    def save(self, entity: T) -> T:
        # Implementation
        pass
    
    def list_all(self) -> List[T]:
        # Implementation
        pass

# Usage
user_repo = Repository(User)
users: List[User] = user_repo.list_all()
```

### 6. Protocol and Structural Subtyping

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict:
        ...

def serialize(obj: Serializable) -> str:
    """Serialize any object that implements to_dict."""
    import json
    return json.dumps(obj.to_dict())

# Works with any class that has to_dict method
class User:
    def to_dict(self) -> dict:
        return {"name": "Alice"}

class Event:
    def to_dict(self) -> dict:
        return {"title": "Concert"}

serialize(User())   # OK
serialize(Event())  # OK
```

### 7. mypy Configuration

```ini
# mypy.ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True

[mypy-services.*]
# Allow untyped definitions in services for gradual migration
disallow_untyped_defs = False

[mypy-tests.*]
# Be more lenient in tests
disallow_untyped_defs = False
check_untyped_defs = False
```

### 8. Running mypy

```bash
# Check all Python files
mypy .

# Check specific directory
mypy services/

# Watch mode (with mypy-watch)
mypy --watch services/

# Generate HTML report
mypy --html-report mypy-report services/
```

## Common Pitfalls

1. **Missing return types** - Always specify return types for functions
2. **Using `Any` too much** - Avoid `Any`; use specific types when possible
3. **Forgetting `Optional`** - Use `Optional[T]` or `T | None` for nullable values
4. **Not using type guards** - Use `isinstance()` checks to narrow types
5. **Ignoring mypy errors** - Fix all mypy errors before merging

## References

- [Python typing module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
