---
description: Start the backend stack for ticketremaster-b
---

// start-backend

## Steps
1. Navigate to the `ticketremaster-b` repository root.
2. Run the command `docker-compose up -d` to start the PostgreSQL and Redis containers.
3. Activate the Python virtual environment: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows).
4. Run database migrations: `flask db upgrade`
5. Start the Flask server: `flask run --host=0.0.0.0`
6. Verify the server is running by accessing `http://localhost:5000/health`.

## Troubleshooting
- If migrations fail, ensure the database container is healthy.
- If port 5000 is in use, verify no other instances are running.