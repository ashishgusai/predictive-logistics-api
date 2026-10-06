from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, get_db

# Create the database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Predictive Logistics API",
    description="Uses Machine Learning to dynamically cluster and optimize delivery routes.",
    version="0.1.0"
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Checks API health and database connectivity."""
    # Simple query to ensure the DB is connected
    stop_count = db.query(models.DeliveryStop).count()
    return {"status": "healthy", "pending_deliveries": stop_count}