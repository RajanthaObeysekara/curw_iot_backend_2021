import hashlib
import json
#import logger 
import Login.loger as logger
#configurations
import Configurations.config as config

def generate_data(*args):
    #add data into seperate variables
    try:
        station_data = args[0]
    except KeyError as e:
        logger.log(log_type=config.log_error,params=e)
        return None
    #extract all variables from data
    """
    There are the Parameters need to be extracted from the packet
    
    Weather Parameters
        1 - dateist
        2 - dailyrainMM
        3 - rain
        4 - tempc
        5 - winddir
        6 - windspeedkmh
        7 - humidity
        8 - baromMM

    Technical Parameters
        1 - batt
        2 - network
        3 - RSSI
        4 - action
        5 - softwaretype
        6 - version
    """
    data_hashed = dict()
    #data_hashed['dateist']=generate_id('dateist',station_data['station_id'])
    data_hashed['dailyrainMM']=generate_id('dailyrainMM',station_data['station_id'])
    data_hashed['rain']=generate_id('rain',station_data['station_id'])
    data_hashed['tempc']=generate_id('tempc',station_data['station_id'])
    data_hashed['winddir']=generate_id('winddir',station_data['station_id'])
    data_hashed['windspeedkmh']=generate_id('windspeedkmh',station_data['station_id'])
    data_hashed['humidity']=generate_id('humidity',station_data['station_id'])
    data_hashed['baromMM']=generate_id('baromMM',station_data['station_id'])
    data_hashed['BAT']=generate_id('BAT',station_data['station_id'])
    data_hashed['network']=generate_id('network',station_data['station_id'])
    data_hashed['RSSI']=generate_id('RSSI',station_data['station_id'])
    data_hashed['action']=generate_id('action',station_data['station_id'])
    data_hashed['softwareType']=generate_id('softwareType',station_data['station_id'])
    data_hashed['version']=generate_id('version',station_data['station_id'])
    return data_hashed    



    
def generate_id(parameter,station_id):
    meta_data= parameter+station_id
    #generate all the keys for the has ids
    hash_id = hashlib.sha256(config.encryption_key)
    hash_id.update(json.dumps(meta_data).encode())
    return hash_id.hexdigest()
    