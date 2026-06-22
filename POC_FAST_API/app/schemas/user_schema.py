from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    """API response schema for user details."""

    id: int = Field(..., example=10001)
    first_name: str = Field(..., example="Promit")
    last_name: str = Field(..., example="Majumder")
    email: EmailStr = Field(..., example="promit.majumder@example.com")
    role: str = Field(..., example="Lead Software Engineer")
    department: str = Field(..., example="Engineering")
    active: bool = Field(..., example=True)


class ErrorResponse(BaseModel):
    """Standard API error response schema."""

    error_code: str
    message: str
