from pydantic import BaseModel, Field


class ReasoningBaseModel(BaseModel):
    reasoning: str = Field(..., description="Before your outputs, write down your chain of thought into this field.")
