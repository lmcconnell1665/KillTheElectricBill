#!/usr/bin/python
import logging

import os
import requests

# So that the CRON job runs from the right working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger('Nest Logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('db_log.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

project_id = os.getenv('PROJECT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'https://www.google.com'
device_0_name = os.getenv('TSTAT_DEVICE_NAME')

def get_nest_status():    
    with open('access_token.txt', 'r') as file:
        access_token = file.read()

    with open('refresh_token.txt', 'r') as file:
        refresh_token = file.read()

    logger.debug('Loaded access and refresh token from file.')

    #Refresh token

    params = (
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('refresh_token', refresh_token),
        ('grant_type', 'refresh_token'),
    )

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)

    response_json = response.json()
    access_token = response_json['token_type'] + ' ' + response_json['access_token']

    with open('access_token.txt', 'w') as f:
        f.write(access_token)

    with open('refresh_token.txt', 'w') as f:
        f.write(refresh_token)

    logger.debug("New access and refresh tokens retrieved and saved.")

    # Get device stats

    url_get_device = 'https://smartdevicemanagement.googleapis.com/v1/' + device_0_name

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token,
    }

    response = requests.get(url_get_device, headers=headers)

    if response.ok:
        logger.debug("Results successfully retrieved.")

    response_json = response.json()

    humidity = response_json['traits']['sdm.devices.traits.Humidity']['ambientHumidityPercent']
    temperature = response_json['traits']['sdm.devices.traits.Temperature']['ambientTemperatureCelsius']
    fan = response_json['traits']['sdm.devices.traits.Fan']['timerMode']
    mode = response_json['traits']['sdm.devices.traits.ThermostatMode']['mode']
    eco = response_json['traits']['sdm.devices.traits.ThermostatEco']['mode']
    hvac = response_json['traits']['sdm.devices.traits.ThermostatHvac']['status']
    setpoint = response_json['traits']['sdm.devices.traits.ThermostatTemperatureSetpoint']['heatCelsius']

    logger.info(f'Indoor temperature is {temperature} celsius.')

    query = f"insert into nest_data (humidity, temperature, fan, mode, eco, hvac, setpoint) values ({humidity}, {temperature}, '{fan}', '{mode}', '{eco}', '{hvac}', {setpoint});"
    logger.debug(f'Returning query: {query}')

    return query