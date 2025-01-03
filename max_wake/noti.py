import json
import smtplib
from config import settings

def send_email(message):
    subject = "TGV MAX ALERT"

    msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (settings.email, ", ".join(settings.destination), subject, message)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(settings.email, settings.password)
    server.sendmail(settings.email, settings.destination, msg)
    server.quit()