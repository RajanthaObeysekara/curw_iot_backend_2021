import json
from flask import app
import DB_connection.query_executer as executor
import Configurations.config as config
import Login.loger as logger

#login con

class validate_station(object):
    def get_station(id,password):
        #execute comparison query for the station

        #TODO add station data into mem cash
        
        #logger.log(log_type=config.log_info,params=None)
        params={'id':id}
        station_data=executor.execute_query(sql_query=config.get_station_query,params=params,query_type=config.db_fetch,query_reason='Fetch Station data')
        if station_data is not None:
            if(station_data['station_password'] == password):
                #station validation is success 
                logger.log(log_type=config.log_info,params='Station Validation is Success')
                return station_data
            else:
                
                logger.log(log_type=config.log_error,params='Station Validation is Unsuccess')
                return None
        else:
            logger.log(log_type=config.log_error,params=f'Station Validation is Unsuccess No station found Under ID = {id}')
            return None 


        #validatestation
        #return station data 