import datetime
#insert database adapter
import DB_connection.query_executer as executor

#import config
import Configurations.config as config

#import logger 
import Login.loger as logger


def warnning_checker(station,data_values):
    #get defined level for station
    #print("warnning checker started")
    #print(station)
    #print(data_values)

    #get defined parrameter list from "parameter_station_notification_fileter"
    params = {"station_id":station.get('id',None)}    
    parameter_def = executor.execute_query(sql_query=config.get_station_parameter_filters,params=params,query_type=config.db_fetch_all,query_reason='Get defined parameters from the parameter_station_notification_fileter')
    #print(type(data_values))
    if len(parameter_def) == 0 :
        #get global station data from the station parameter table
        parameter_def = executor.execute_query(sql_query=config.get_station_parameter_filters_global,params=params,query_type=config.db_fetch_all,query_reason='Get defined parameters from the Global stations')
        pass
    for item in parameter_def:
        parameter_id = item.get('parameter_id')
        parameter = item.get('parameter')
        parameter_upper = item.get('upper_boundary')
        parameter_lower = item.get('lower_boundary')
        parameter_value=data_values.get(str(parameter),None)
        #print(parameter_value)
        #print(parameter_upper)
        #print(parameter_lower)
        #adding conditional comparissions
        warnning_status = None
        
        if parameter_value != None : #checking parameter values
            if((float(parameter_value) > parameter_upper)):
                warnning_status = config.warning_exceed
                #add to the next function
                insert_warnings(station_id=station.get('id',None),parameter=parameter,value=parameter_value,margin=parameter_upper,warning_status=warnning_status,parameter_id=parameter_id)
                logger.log(log_type=config.warning_exceed,params=f'Parameter - {parameter} | Parameter_ID-{parameter_id} | Upper_boundry_level-{parameter_upper} | parameter_value-{parameter_value} | exceeded_value +{float(parameter_value) - float(parameter_upper)}')

            if(float(parameter_value)  < parameter_lower):
                warnning_status = config.warning_below
                #add to the next function
                insert_warnings(station_id=station.get('id',None),parameter=parameter,value=parameter_value,margin=parameter_lower,warning_status=warnning_status,parameter_id=parameter_id)
                logger.log(log_type=config.warning_below,params=f'Parameter - {parameter} | Parameter_ID-{parameter_id} | Lower_boundry_level-{parameter_upper} | parameter_value-{parameter_value} | exceeded_value -{float(parameter_lower) - float(parameter_value)}')
                #TODO
            if(float(parameter_value) >= parameter_lower and float(parameter_value)  <= parameter_upper):
                warning_status = config.warning_normal
                logger.log(log_type=config.warning_normal,params=f'Parameter - {parameter} | Parameter_ID-{parameter_id} | Lower_boundry_level-{parameter_upper} | parameter_value-{parameter_value} | exceeded_value -{float(parameter_lower) - float(parameter_value)}')
                #add to the next function
                #add log file into
                #TODO
    pass

def insert_warnings(station_id,parameter,value,margin,warning_status,parameter_id):
    warning_time = datetime.datetime.now().replace(microsecond=0)
    params={"station_id":station_id,"parameter_id":parameter_id,"time":warning_time,"value":value,"margin_level":margin,"warning_status":warning_status}
    insert_result = executor.execute_query(sql_query=config.insert_station_warnnings,params=params,query_type=config.db_insert,query_reason=f"Insert Warnning into station warnning table. parameter = {parameter} ,warnning_time = {warning_time}")
    return
