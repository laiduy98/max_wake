import datetime
from fastapi import HTTPException


def is_args_valid(args):
    try:
        datetime.datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("\033[31mIncorrect data format, should be YYYY-MM-DD\033[0m")

    if (args.alert != "SMS" and args.alert != "EMAIL" and args.alert != "NO"):
        print ("\033[31mAlert bad formatted\033[0m")
        raise HTTPException


    hour = args.hour.split(':', 1)
    if (int(hour[0]) > 0 and int(hour[0]) < 24 and int(hour[1]) > 0 and int(hour[1]) < 60):
        return hour
    print ("\033[31mHour bad formatted\033[0m")
    
