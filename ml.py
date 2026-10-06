import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
import models

def calculate_delivery_zones(db: Session, num_drivers: int):
    """
    Fetches pending deliveries, clusters them geographically, 
    and updates the database with the assigned zones.
    """
    # 1. Fetch unassigned/pending deliveries from the DB
    deliveries = db.query(models.DeliveryStop).filter(models.DeliveryStop.is_delivered == False).all()
    
    if not deliveries:
        return 0
        
    # Prevent errors if there are more drivers than actual deliveries
    n_clusters = min(num_drivers, len(deliveries))
    
    # 2. Format data for Scikit-Learn (NumPy Array of [lat, lng])
    coords = np.array([[d.latitude, d.longitude] for d in deliveries])
    
    # 3. Initialize and train the K-Means model
    # random_state ensures reproducible results for testing
    # n_init=10 runs the algorithm 10 times with different centroids to find the best fit
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(coords)
    
    # 4. Assign the resulting cluster labels back to our database models
    for i, delivery in enumerate(deliveries):
        # labels_ returns an array like [0, 1, 0]. We add 1 for user-friendly 1-indexed zones
        delivery.assigned_zone = int(kmeans.labels_[i]) + 1
        
    # 5. Commit changes to the database
    db.commit()
    
    return len(deliveries)