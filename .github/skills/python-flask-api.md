---
name: python-flask-api
description: Building REST APIs with Flask - patterns, conventions, and best practices
technologies: [Python, Flask, REST]
repositories: [ticketremaster-b, source-repo-code]
---

# Python Flask API Development

## When to Use

Use this skill when creating or modifying Flask REST API endpoints in Python services.

## Prerequisites

- Python 3.12+
- Basic understanding of HTTP methods and REST principles
- Familiarity with Flask framework

## Step-by-Step Instructions

### 1. Project Structure

Organize Flask services with clear separation of concerns:

```
service-name/
├── app.py              # Application factory
├── routes.py           # Route definitions
├── models.py           # Database models
├── schemas.py          # Request/response schemas
├── services.py         # Business logic
├── requirements.txt    # Dependencies
└── tests/              # Unit tests
```

### 2. Application Factory Pattern

```python
# app.py
from flask import Flask
from routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    # Health check endpoint
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "service-name"}, 200
    
    return app
```

### 3. Route Definitions

```python
# routes.py
from flask import Blueprint, jsonify, request

bp = Blueprint("resources", __name__)

@bp.get("/resources")
def list_resources():
    """List all resources with optional filtering."""
    resources = get_all_resources()
    return jsonify({"data": resources}), 200

@bp.get("/resources/<resource_id>")
def get_resource(resource_id):
    """Get a specific resource by ID."""
    resource = get_resource_by_id(resource_id)
    if not resource:
        return jsonify({
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": "Resource not found."
            }
        }), 404
    return jsonify({"data": resource}), 200

@bp.post("/resources")
def create_resource():
    """Create a new resource."""
    data = request.get_json()
    if not data:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request body is required."
            }
        }), 400
    
    resource = create_new_resource(data)
    return jsonify({"data": resource}), 201
```

### 4. Consistent Response Format

Always use consistent JSON response structures:

**Success Response:**
```python
return jsonify({"data": result}), 200
```

**Error Response:**
```python
return jsonify({
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message."
    }
}), status_code
```

### 5. Error Handling

```python
# services.py
class ResourceNotFoundError(Exception):
    def __init__(self, resource_id):
        self.resource_id = resource_id
        super().__init__(f"Resource {resource_id} not found")

# routes.py
@bp.get("/resources/<resource_id>")
def get_resource(resource_id):
    try:
        resource = get_resource_by_id(resource_id)
        return jsonify({"data": resource}), 200
    except ResourceNotFoundError:
        return jsonify({
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": f"Resource {resource_id} not found."
            }
        }), 404
```

### 6. Request Validation

```python
from marshmallow import Schema, fields, validate

class CreateResourceSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=False, allow_none=True)
    type = fields.Str(required=True, validate=validate.OneOf(["type1", "type2"]))

create_schema = CreateResourceSchema()

@bp.post("/resources")
def create_resource():
    data = request.get_json()
    
    # Validate request
    try:
        validated_data = create_schema.load(data)
    except ValidationError as err:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": err.messages
            }
        }), 400
    
    resource = create_new_resource(validated_data)
    return jsonify({"data": resource}), 201
```

## Common Pitfalls

1. **Inconsistent error formats** - Always use the same error structure
2. **Missing health endpoints** - Every service needs `/health`
3. **No request validation** - Always validate input data
4. **Mixing concerns** - Keep routes, models, and business logic separate
5. **Not handling None values** - Always check for None before accessing attributes

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [Error Handling in Flask](https://flask.palletsprojects.com/en/2.3.x/errorhandling/)
