from flask import Flask,request
from flask_restful import Resource,Api
#database insertion
from DB_connection import cruw_database

#validation
from Validation import station,generate_id

#date time import 
from datetime import datetime

#configurations
import Configurations.config as config

#import logger 
import Login.loger as logger



#keep starting time
start_time = datetime.now()

app = Flask(__name__)
api=Api(app)


class WeatherData(Resource):
   def get(self):
      return_data = {
      'Welcome Message' : 'Backend Server MCUDP Weather Station',
      'Current Server Time': str(datetime.now()),
      'Server Started time' : str(start_time)
      }
      return return_data,200

   def post(self):
      data = request.get_json(silent=True)
      #fed into raw database
      #TODO add each variable into seperate variable and data raw data as a seperate collection
      
      logger.insert_raw_packet(log_request=data,reqst_ip=request.remote_addr)
      #check data availability
      if data is not None:
         #ValidateStation( validate_object ) #this will validate the station with credentials
         station_data=station.validate_station.get_station(id =data.get('ID',None),password=data.get('PASSWORD',None))
         if station_data is not None:
            #TODO validate each Parameter seperately
            
            #generate hash id with date embedded
            data_hashed_id = generate_id.generate_data(station_data)
            if( data_hashed_id is not None):
               #hash id entered successfuly
               logger.log(log_type=config.log_info,params=f'Hash IDs Generated {id} {datetime.now()}')

               #Insert data into database
               inserted_data = cruw_database.insert_database(hash_id=data_hashed_id,data_values=data,station=station_data)

               return 'Data Entered',200
            else:
               return 'Fail Data Inserting', 403
            
         #TODO validate, hashdata , normalize , enter into sql
         else:
            return 'Station Validation Fail', 401
         
      else:
         return 'Invalid Input', 400

      

api.add_resource(WeatherData,'/weatherstation/updateweatherstation') #pushing weather data url ex:- http://124.43.5.187:27017/weatherdata


#information anout the get request 
#weather station data post request 

app.run(port=5000,debug=True)
