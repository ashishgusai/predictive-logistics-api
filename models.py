from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class DeliveryStop(Base):
    __tablename__ = "delivery_stops"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    address = Column(String)
    
    # Latitude and Longitude for ML geographic clustering
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Has this delivery been completed?
    is_delivered = Column(Boolean, default=False)
    
    # Which driver zone (cluster) this belongs to, assigned by our ML model
    assigned_zone = Column(Integer, nullable=True)