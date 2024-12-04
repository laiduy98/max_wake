from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# from sqlmodel import 

app = FastAPI()

class TripInformation(BaseModel):
    origin: str
    destination: str
    search_date: str
    search_hour_start: Optional[str] = None
    search_hour_end: Optional[str] = None


@app.get('/')
def read_root():
    return {"message": "Max Wake is working"}

@app.post('/add_search_trip')
def add_trip(trip: TripInformation):

    
    return {'origin': trip.origin, 'destination': trip.destination, 'date': trip.search_date, 'hour': trip.search_hour_start}
    
