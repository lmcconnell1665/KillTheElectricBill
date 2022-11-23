#!/usr/bin/python
import logging

import os
import requests

# So that the CRON job runs from the right working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger('Weather Logger')
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


def get_weather():

    response = requests.get('https://api.weather.gov/gridpoints/OHX/49,60/forecast')

    if response.ok:
        logger.debug("Successfully got the weather.")
    else:
        logger.error("Failed to get weather.")
        return

    json_data = response.json()

    updatedTime = json_data['properties']['updated']
    forecastFor = json_data['properties']['periods'][0]['name']
    temp = json_data['properties']['periods'][0]['temperature']
    windSpeed = json_data['properties']['periods'][0]['windSpeed']
    windDirection = json_data['properties']['periods'][0]['windDirection']
    icon = json_data['properties']['periods'][0]['icon']
    shortForecast = json_data['properties']['periods'][0]['shortForecast']
    detailedForecast = json_data['properties']['periods'][0]['detailedForecast']

    logger.info(f'Outdoor temperature is {temp} fahrenheit.')

    query = f"insert into weather_data (forecast_updated, forecast_for, temp, wind_speed, wind_direction, icon, short_forecast, detailed_forecast) values ('{updatedTime}', '{forecastFor}', {temp}, '{windSpeed}', '{windDirection}', '{icon}', '{shortForecast}', '{detailedForecast}');"
    logger.debug(f'Returning query: {query}')

    return query


if __name__ == '__main__':
    get_weather()