from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(
        min_length=1,  # Minimum length of 1 character
        max_length=100,  # Maximum length of 100 characters
        description="Name of the item must be between 1 and 100 characters"
    )
    price: float = Field(
        ge=0,  # Greater than or equal to 0
        le=10000,  # Less than or equal to 10000
        description="Price of the item must be a positive number"
    )
