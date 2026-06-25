from pydantic import Field
from pydantic import BaseModel


class PDFAcceptModel(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    """Standard API error response schema."""

    error_code: str
    message: str