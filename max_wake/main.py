from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from check_params import is_info_valid
from sqlmodel import SQLModel, create_engine, Session, Field, select
import requests
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
import threading
from config import settings
import uvicorn

app = FastAPI()

class TripInformation(BaseModel):
    origin: str
    destination: str
    date: str
    hour_start: Optional[str] = None
    hour_end: Optional[str] = None
    alert: Optional[str] = None

class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origin: str
    destination: str
    date: str
    hour_start: Optional[str] = None
    hour_end: Optional[str] = None
    alert: Optional[str] = None

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

@app.get('/')
def read_root():
    return {"message": "Max Wake is working"}

@app.post('/add_search_trip')
def add_trip(trip: TripInformation):

    is_info_valid(trip_info=trip)
    print(trip)
    trip_record = Trip(
    origin=trip.origin,
    destination=trip.destination,
    date=trip.date,
    hour_start=trip.hour_start,
    hour_end=trip.hour_end,
    alert=trip.alert
    )

    with Session(engine) as session:
        session.add(trip_record)
        session.commit()
        session.refresh(trip_record)
    
    return {"message": "Trip added successfully",
            "trip": trip_record}
    
def check_sncf_api(trip: Trip):
    # Replace with actual SNCF API endpoint and parameters
    url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination"
    url += "&refine.origine=" + trip.origin
    url += "&refine.destination=" + trip.destination
    url += "&refine.date=" + trip.date
    api_url = url.replace(" ", "%20")
    response = requests.get(api_url)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        # Check if there are available tickets
        if search_train(data, trip) == True:
            return True
    return False

# def send_email(subject, body, to_email):
#     from_email = settings.email
#     password = settings.password

#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     server = smtplib.SMTP("smtp.example.com", 587)
#     server.starttls()
#     server.login(from_email, password)
#     text = msg.as_string()
#     server.sendmail(from_email, to_email, text)
#     server.quit()

# def send_alert(data, args):
#     message = "Train disponible " + data["fields"]["date"] + " !\n" +\
#     "Aller : " + data["fields"]["origine"] +\
#     "\nDepart a : " + data["fields"]["heure_depart"] +\
#     "\nRetour : " + data["fields"]["destination"] +\
#     "\nArrive a : " + data["fields"]["heure_arrivee"]
#     print ("\033[32m" + message + "\033[0m\n")
#     if (args.alert == "email"):
#         print(message)
#         send_email(message)

def search_train(data, trip):
    alert = False
    nb_train = len(data["records"])
    for i in range(0, nb_train):
        if (data["records"][i]["fields"]["od_happy_card"] == "OUI"):
            hour = data["records"][i]["fields"]["heure_depart"]
            hourIn = int(hour.split(':', 1)[0])
            if (int(trip.hour_start) <= hourIn and int(trip.hour_end) >= hourIn):
                # send_alert(data["records"][i], trip)
                alert = True
    if (alert == True):
        return True
    return False

def check_and_notify():
    print('checking...')
    with Session(engine) as session:
        trips = session.exec(select(Trip)).all()
        print(trips)
        for trip in trips:
            if check_sncf_api(trip):
                print(f"Train ticket from {trip.origin} to {trip.destination} on {trip.date} is available.")
                # send_email(
                #     subject="Train Ticket Available",
                #     body=f"Train ticket from {trip.origin} to {trip.destination} on {trip.date} is available.",
                #     to_email="user@example.com"
                # )
            else:
                print(f"No Max Jeune train ticket found from {trip.origin} to {trip.destination} on {trip.date}.")
                # send_email(
                #     subject="No Max Jeune Train Ticket Found",
                #     body=f"No Max Jeune train ticket found from {trip.origin} to {trip.destination} on {trip.date}.",
                #     to_email="user@example.com"
                # )

# Schedule the check every 30 minutes
def run_scheduler():
    print('start')
    schedule.every(1).seconds.do(check_and_notify)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Run the scheduler
    # scheduler_thread = threading.Thread(target=run_scheduler)
    # scheduler_thread.daemon = True
    # scheduler_thread.start()

    run_scheduler()

    # uvicorn.run(app, host="0.0.0.0", port=8000)