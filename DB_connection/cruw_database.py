import psycopg2.extras
import DB_connection.query_executer as executor
import datetime
#import config
import Configurations.config as config
#import logger 
import Login.loger as logger
#warning and notification
from Notification import warning_notification

def insert_database(hash_id,data_values,station):

    #update run database 
    #    -lora validation with logic 

    #lora validation
    network_type = data_values['health'].get('network',None)
    station_id = data_values.get('ID',None)

    # 1. get date time period of the last data point
    params = {"id":station['id']}
    time_from_database=executor.execute_query(sql_query=config.get_time_query,params=params,query_type=config.db_fetch,query_reason='Get last Time from Run Table')
    logger.log(log_type=config.log_info,params=f'Last data insert time fetch {time_from_database}')

  
    if(time_from_database is None):
        #insert new data into run table not existing new data
        time_from_database = datetime.datetime(2000,1,1,00,00,00,00) #data variable generate for validation
        pass
    else:
        time_from_database= time_from_database.get('originate_time',None)
    
    #if tme from database is not available 
    if time_from_database is None:
        logger.log(log_type=config.log_error,params=f'time from data base none error')
        return None
    flat_data_values= flat_data(data_values=data_values)

    #pushing notification
    warning_notification.warnning_checker(data_values=flat_data_values,station=station)

    #covnert data packet`s string to date time 
    date_time_obj = datetime.datetime.strptime(data_values['data'][0]['dateist'], '%Y-%m-%d %H:%M:%S')

    if (date_time_obj == time_from_database):
        #duplicate data point no need to add to the server
        #add record for the duplicate data points
        logger.log(log_type=config.log_info,params=f"Duplicate Data Record -> {station_id}-Station ID , Network Type - {network_type} , Duplicate time period - {time_from_database} " )
        pass
    
    if (date_time_obj > time_from_database):
        #new record data should be added to the database
        #updating run
        logger.log(log_type=config.log_info,params=f"New Data Record -> Station ID - {station_id}, Network Type - {network_type}- {str(flat_data_values['dateist'])}   " )
        for key in hash_id.keys():
            params={"hash_id_key":hash_id[key],"flat_data_values_id":flat_data_values['ID'],"flat_data_values_dateiskey":flat_data_values['dateist'],"key":key,"flat_data_values_key":flat_data_values[key]}
            executor.execute_query(sql_query=config.insert_into_run,params=params,query_type=config.db_insert,query_reason=f"Upsert run Table for new Data Record - {str(hash_id[key])} - {str(flat_data_values['ID'])} - {str(key)} - {str(flat_data_values[key])}")
        #updating data
            executor.execute_query(sql_query=config.insert_into_data,query_type=config.db_insert,params=params,query_reason=f"Insert into data Table for new Data Record - {str(hash_id[key])} - {str(flat_data_values['ID'])} - {str(key)} -{str(flat_data_values[key])} ")
            
            if(key == 'rain'):
                #index for count rain ticks
                count_index = 0
                for tick in flat_data_values.get('rain_data',None):
                    params_rain_ticks={"has_id_key":hash_id[key],"count_index":count_index,"tick":tick}
                    executor.execute_query(sql_query=config.insert_into_rain_ticks,params=params_rain_ticks,query_type=config.db_insert,query_reason=f"Insert into rain_ticks Table for new Data record - {str(hash_id[key])} - {str(count_index)} -{str(tick)}")
                    count_index += 1
                pass
        
        pass

    if (date_time_obj < time_from_database):
        #old record should be validate with the existing data items
        #TODO check validity of the data object where parameter if from hash object and time from dateist (upsert)
        #TODO add record into missing record database

        #check from data table
        logger.log(log_type=config.log_info,params=f"Late Arrive Data Record -> {station_id}-Station ID , Network Type - {network_type}  - {str(flat_data_values['dateist'])} " )
        params_check_record = {"hash_id_network":hash_id['network'],"flat_data_values_time":flat_data_values['dateist']}
        previous_record=executor.execute_query(sql_query=config.previous_record_check,params=params_check_record,query_type=config.db_fetch,query_reason=f"Check Previous Record from data table - {str(station_id)} ")
        if(previous_record is not None):
            #duplicate data packet from different network
            logger.log(log_type=config.log_info,params=f"Duplicate packet from -> {station_id}-Station ID , Network Type - {network_type} - exist record network type - {previous_record}" )
            pass
        else:
            #missed record therefore insrt into database
            logger.log(log_type=config.log_info,params=f"Missed data packet from -> {station_id}-Station ID , Network Type - {network_type} - exist record network type - {previous_record}" )
            params={"hash_id_key":hash_id[key],"flat_data_values_id":flat_data_values['ID'],"flat_data_values_dateiskey":flat_data_values['dateist'],"key":key,"flat_data_values_key":flat_data_values[key]}
            executor.execute_query(sql_query=config.insert_into_run,params=params,query_type=config.db_insert,query_reason=f"Upsert run Table for new Data Record - {str(hash_id[key])} - {str(flat_data_values['ID'])} - {str(key)} - {str(flat_data_values[key])}")
            pass


        pass

    
    pass 

def flat_data(data_values=None):

    flat_data_values = dict()
    flat_data_values['ID']= data_values.get('ID',None)
    
    #data
    flat_data_values['dateist']= data_values['data'][0].get('dateist',None)
    flat_data_values['dailyrainMM']= data_values['data'][0].get('dailyrainMM',None)
    flat_data_values['rain']= len(data_values['data'][0].get('rain',None))
    flat_data_values['rain_data']=data_values['data'][0].get('rain',None)
    flat_data_values['tempc']= data_values['data'][0].get('tempc',None)
    flat_data_values['winddir']= data_values['data'][0].get('winddir',None)
    flat_data_values['windspeedkmh']= data_values['data'][0].get('windspeedkmh',None)
    flat_data_values['humidity']= data_values['data'][0].get('humidity',None)
    flat_data_values['baromMM']= data_values['data'][0].get('baromMM',None)
    
    #health
    flat_data_values['BAT']= data_values['health'].get('BAT',None)
    flat_data_values['network']= data_values['health'].get('network',None)
    flat_data_values['RSSI']= data_values['health'].get('RSSI',None)
    
    #description
    flat_data_values['action']= data_values.get('action',None)
    flat_data_values['softwareType']= data_values.get('softwareType',None)
    flat_data_values['version']= data_values.get('version',None)

    return flat_data_values


