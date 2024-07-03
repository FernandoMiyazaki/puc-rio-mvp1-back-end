from pydantic import BaseModel

class MessageSchema(BaseModel):
    """
    Schema representing a simple message response.

    This schema is used for responses that only contain a message field.
    It is typically used for endpoints that perform actions such as deletions or updates where a detailed response is not necessary.

    Attributes:
        message (str): A descriptive message indicating the result of the operation.

    Example:
        {
            "message": "Operation completed successfully."
        }
    """
    message: str
