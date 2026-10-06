from pydantic import BaseModel
from typing import Optional

# Shared properties
class DeliveryStopBase(BaseModel):
    customer_name: str
    address: str
    latitude: float
    longitude: float

# Properties to receive on item creation
class DeliveryStopCreate(DeliveryStopBase):
    pass

# Properties to return to the client
class DeliveryStopResponse(DeliveryStopBase):
    id: int
    is_delivered: bool
    assigned_zone: Optional[int] = None

    # This config tells Pydantic to read data even if it is an ORM model
    model_config = {"from_attributes": True}