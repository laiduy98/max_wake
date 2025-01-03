import datetime
from fastapi import HTTPException


def is_info_valid(trip_info):
    try:
        datetime.datetime.strptime(trip_info.date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    if (trip_info.alert != "email" and trip_info.alert != "no"):
        # print ("\033[31mAlert bad formatted\033[0m")
        raise HTTPException(status_code=418, detail="Alert bad formatted, should be email/no")


    # hour = trip_info.hour.split(':', 1)
    # if (int(hour[0]) > 0 and int(hour[0]) < 24 and int(hour[1]) > 0 and int(hour[1]) < 60):
    #     return hour
    # print ("\033[31mHour bad formatted\033[0m")

    # hour = trip_info.hour.split(':', 1)
    if not (int(trip_info.hour_start) > 0 
            and int(trip_info.hour_end) < 24 
            and int(trip_info.hour_end) > 0 
            and int(trip_info.hour_end) < 24 
            and int(trip_info.hour_start) < int(trip_info.hour_end)):
        raise HTTPException(status_code=418, detail="Hour bad formatted")
    
