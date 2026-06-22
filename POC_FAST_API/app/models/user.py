from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """Internal domain model representing a user."""

    id: int = Field(..., description="Unique user identifier")
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    department: str
    active: bool = True
