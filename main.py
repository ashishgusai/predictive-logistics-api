from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

from pydantic import BaseModel
from ml import calculate_delivery_zones


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Predictive Logistics API",
    description="Uses Machine Learning to dynamically cluster and optimize delivery routes.",
    version="0.2.0"
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    stop_count = db.query(models.DeliveryStop).count()
    return {"status": "healthy", "pending_deliveries": stop_count}

@app.post("/api/v1/deliveries", response_model=schemas.DeliveryStopResponse)
def create_delivery(delivery: schemas.DeliveryStopCreate, db: Session = Depends(get_db)):
    """Ingest a new delivery request."""
    # Convert Pydantic schema to SQLAlchemy model instance
    db_delivery = models.DeliveryStop(
        customer_name=delivery.customer_name,
        address=delivery.address,
        latitude=delivery.latitude,
        longitude=delivery.longitude
    )
    
    # Save to database
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery) # Reloads the object to get the generated ID
    
    return db_delivery

@app.get("/api/v1/deliveries", response_model=List[schemas.DeliveryStopResponse])
def get_pending_deliveries(db: Session = Depends(get_db)):
    """Fetch all deliveries that haven't been completed yet."""
    deliveries = db.query(models.DeliveryStop).filter(models.DeliveryStop.is_delivered == False).all()
    return deliveries

class ClusterRequest(BaseModel):
    num_drivers: int

@app.post("/api/v1/cluster-routes")
def optimize_routes(request: ClusterRequest, db: Session = Depends(get_db)):
    """
    Run ML clustering to group deliveries into optimized driver zones.
    """
    try:
        updated_count = calculate_delivery_zones(db, request.num_drivers)
        
        if updated_count == 0:
            return {"message": "No pending deliveries to cluster."}
            
        return {
            "message": f"Successfully clustered {updated_count} deliveries into {request.num_drivers} zones."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))