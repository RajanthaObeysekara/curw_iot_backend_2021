from datetime import datetime
import Configurations.config as config
from pymongo import MongoClient
#encryption
import hashlib
import json



def log(log_type=None,params=None):
    current_time= datetime.now()
    if(log_type == config.log_critical):
        insert_log_data(log_type=config.log_critical,log_data=params)
        return
    if(log_type == config.log_error):
        insert_log_data(log_type=config.log_error,log_data=params)
        return
    if(log_type == config.log_info):
        insert_log_data(log_type=config.log_info,log_data=params)
        return
    if(log_type == config.log_duplicate):
        insert_log_data(log_type=config.log_duplicate,log_data=params)
        return
    return True

def insert_log_data(log_type=None,log_data=None):
    #create packet
    log_message = dict()
    log_message['timestamp'] = datetime.now()
    log_message['type'] = log_type
    log_message['log_data'] = log_data
    #insert into database
    #database inserting 
    client=MongoClient(config.mongo_db_connection)
    db = client['Curw-Log-Data']
    #create collection name
    collection_date = str(get_date_Mongo())
    collection = db[collection_date]
    x = collection.insert_one(log_message)
    return x.inserted_id


def insert_raw_packet(log_request=None,reqst_ip = '0.0.0.0'):
    temp_log = dict()
    #serializing data packet
    if log_request is None : 
        temp_log['Empty Request - Error']=f'Empty Request from {reqst_ip}'
    else : 
        temp_log['id'] = log_request.get('ID',None)
        #packet recorded in station
        temp_log['station_record_time'] = log_request['data'][0].get('dateist',None)
        #packet sent from station
        temp_log['server_record_time'] = str(datetime.now())
        temp_log['data'] = log_request.get('data',None)
        temp_log['health'] = log_request.get('health',None)
        temp_log['meta_data'] = {"software_type":log_request.get('softwareType',None),"action":log_request.get('action',None),"version":log_request.get('version',None)}
        ser_pass = log_request['PASSWORD']
        enc_pass = hashlib.sha256(config.encryption_key)
        enc_pass.update(json.dumps(ser_pass).encode())
        ser_pass = enc_pass.hexdigest()
        temp_log['encrypted_password'] = ser_pass
        temp_log['station_public_ip'] = reqst_ip
    
    #database inserting 
    client=MongoClient(config.mongo_db_connection)
    db = client['Curw-Raw-Data']
    #create collection name
    collection_date = str(get_date_Mongo())
    collection = db[collection_date]
    x = collection.insert_one(temp_log)
    return x.inserted_id

def get_date_Mongo():
    return str(datetime.now().date())