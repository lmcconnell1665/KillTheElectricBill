#!/usr/bin/python
import logging

import os
import pyodbc
from nest import *
from weather import *

# So that the CRON job runs from the right working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger('Main Electricity Logger')
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

logger.debug('Starting run.')

class AzureSQL:
    def __init__(self,
                 server: str = '',
                 database: str = 'Home',
                 username: str = 'home_writer',
                 password: str = ''):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};' + \
                                         'SERVER=tcp:' + server + ';PORT=1443;' + \
                                         'DATABASE=' + database + ';Encrypt=YES;TrustServerCertificate=YES;UID=' + username + ';PWD=' + password)

    def __enter__(self):
        logger.debug(f'Calling __enter__ method to {self.server} server')
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, trace):
        logger.debug(f'Calling __exit__ method to {self.server} server')
        self.connection.commit()
        self.connection.close()


def save_data(query):

    with AzureSQL() as cursor:
        try:
            cursor.execute(query)
            logger.info(f'SQL query successfully run.')

        except:
            logger.error(f"Error running query: {query}")


if __name__ == '__main__':
    nest_query = get_nest_status()
    weather_query = get_weather()
    save_data(nest_query)
    save_data(weather_query)