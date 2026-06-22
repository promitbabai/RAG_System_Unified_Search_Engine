# FastAPI User Service - Production-Ready Layered Architecture

A basic but production-style FastAPI project that exposes a REST endpoint to retrieve user details by user ID.

The user data is initialized as constants in the DAO layer. There is no database dependency.

## Architecture

```text
Controller -> Service -> DAO -> In-memory constants
```

## Project Structure

```text
fastapi-user-service-production/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── controllers/
│   │       └── user_controller.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── dao/
│   │   └── user_dao.py
│   ├── exceptions/
│   │   ├── custom_exceptions.py
│   │   └── exception_handlers.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user_schema.py
│   └── services/
│       └── user_service.py
├── tests/
│   └── test_user_api.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Setup in VS Code

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For running tests:

```bash
pip install -r requirements-dev.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

## API Endpoint

### Get User Details

```http
GET /api/v1/users/{user_id}
```

Example:

```text
http://127.0.0.1:8000/api/v1/users/10001
```

Sample response:

```json
{
  "id": 10001,
  "first_name": "Promit",
  "last_name": "Majumder",
  "email": "promit.majumder@example.com",
  "role": "Lead Software Engineer",
  "department": "Engineering",
  "active": true
}
```

## Health Check

```http
GET /health
```

## Swagger UI

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest
```

## Error Handling

### User Not Found

```json
{
  "error_code": "USER_NOT_FOUND",
  "message": "User not found for user_id=99999"
}
```

### Validation Error

```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid request input",
  "details": []
}
```

## Notes

This project is intentionally simple but structured for extensibility:

- Replace `UserDAO` with database access later.
- Add service-level business rules in `UserService`.
- Add more endpoints in `api/controllers`.
- Extend exception handling from `exceptions`.
- Externalize configuration using environment variables.
