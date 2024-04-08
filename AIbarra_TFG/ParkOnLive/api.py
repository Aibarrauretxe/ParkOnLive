from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class ParkingOccupancyIn(BaseModel):
    parking_id: int
    occupancy_current: int
    occupancy_max: int

@app.post("/occupancy/")
async def create_parking_occupancy(occupancy_data: ParkingOccupancyIn):
    from ParkOnLive.models import Parking, ParkingOccupancy
    try:
        parking = Parking.objects.get(pk=occupancy_data.parking_id)
    except Parking.DoesNotExist:
        raise HTTPException(status_code=404, detail="Parking not found")
    
    new_occupancy = ParkingOccupancy(
        parking=parking,
        occupancy_current=occupancy_data.occupancy_current,
        occupancy_max=occupancy_data.occupancy_max,
        timestamp=datetime.now()
    )
    new_occupancy.save()
    return {"message": "Parking occupancy created successfully"}