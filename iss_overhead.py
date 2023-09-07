import time

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email_config
from datetime import datetime

MY_LAT = 32.076102
MY_LNG = 34.851810

ISS_URL = "http://api.open-notify.org/iss-now.json"
WEATHER_URL = "https://api.sunrise-sunset.org/json"
DESTINATION_EMAIL = "adrien.allouche@gmail.com"
SUBJECT = "Can you spot the ISS?"
MESSAGE = "Levez les yeux au ciel"

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}


def send_email(message=MESSAGE, subject=SUBJECT, destination_email=DESTINATION_EMAIL):
    # Creation d'un objet multipart comprenant sujet/destinataire/receveur/type de message (plain, html, pic, video,...)
    multipart_message = MIMEMultipart()
    multipart_message["Subject"] = subject
    multipart_message["From"] = email_config.config_email
    multipart_message["To"] = destination_email
    # Rajout du text_body dans le message
    multipart_message.attach(MIMEText(message, "plain"))

    # 1. Creation du server
    server_mail = smtplib.SMTP(email_config.config_server, email_config.config_server_port)

    # 2. Mise en place du protocole de cryptage TLS
    server_mail.starttls()

    # 3. Authentification sur le serveur
    server_mail.login(email_config.config_email, email_config.confg_pwd)

    # 4. Envoi du mail
    server_mail.sendmail(email_config.config_email, destination_email, multipart_message.as_string())

    # 5. Fermeture de la connexion
    server_mail.quit()


def get_response_from_api(url):
    response = requests.get(url=url)

    # Raise exception if error
    response.raise_for_status()

    return response.json()


def get_iss_position(data_from_iss):
    return float(data_from_iss["iss_position"]["longitude"]), float(data_from_iss["iss_position"]["latitude"])


def get_sunrise_hour(data_from_sunrise):
    return int(data_from_sunrise["results"]["sunrise"].split(":")[0])


def get_sunset_hour(data_from_sunrise):
    return int(data_from_sunrise["results"]["sunset"].split(":")[0])


def is_iss_overhead(iss_curr_position, curr_lat=MY_LAT, curr_lng=MY_LNG) -> bool:
    iss_lng, iss_lat = iss_curr_position
    return abs(iss_lat - curr_lat) < 3 and abs(iss_lng - curr_lng) < 3


def is_night_time(sunrise_hour, sunset_hour):
    # Get the current hour value
    time_now = datetime.now().hour
    return time_now >= sunset_hour or time_now <= sunrise_hour


# Get the response from ISS api
data_from_iss = get_response_from_api(ISS_URL)

# Get ISS longitude and latitude
iss_position = get_iss_position(data_from_iss)

# Get the response from sunrise-sunset api
data_from_sunrise = get_response_from_api(WEATHER_URL)

# Get sunrise hour
sunrise_hour = get_sunrise_hour(data_from_sunrise)
sunset_hour = get_sunset_hour(data_from_sunrise)

while True:
    time.sleep(60)
    if is_iss_overhead(iss_curr_position=iss_position) and is_night_time(sunrise_hour=sunrise_hour, sunset_hour=sunset_hour):
        send_email()