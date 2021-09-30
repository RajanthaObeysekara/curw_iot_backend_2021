from decouple import config
#station query
get_station_query = '''SELECT * FROM station WHERE station.station_id =%(id)s '''

#curw database query
get_time_query = '''SELECT originate_time FROM run WHERE run.station = %(id)s '''
insert_into_run = '''INSERT INTO run(id,station,originate_time,parameter_id) VALUES(%(hash_id_key)s,(SELECT id FROM station WHERE station_id=%(flat_data_values_id)s), %(flat_data_values_dateiskey)s,(SELECT parameter.parameter_id FROM parameter WHERE parameter.parameter= %(key)s)) ON CONFLICT (id) DO UPDATE SET originate_time = %(flat_data_values_dateiskey)s '''
insert_into_data= '''INSERT INTO data(id,time,value) VALUES(%(hash_id_key)s,%(flat_data_values_dateiskey)s,%(flat_data_values_key)s) '''
insert_into_rain_ticks='''INSERT INTO rain_ticks (id, rain_tick_no, rain_tick_time) values (%(has_id_key)s,%(count_index)s,%(tick)s) ON CONFLICT (id,rain_tick_time) DO NOTHING'''
previous_record_check = '''SELECT value FROM data WHERE id=%(hash_id_network)s AND time=%(flat_data_values_time)s'''


#Notification database query
get_station_parameter_filters = '''SELECT parameter.parameter_id,upper_boundary,lower_boundary,parameter.parameter FROM parameter INNER JOIN parameter_station_notification_filter ON parameter.parameter_id =parameter_station_notification_filter.parameter_id where station_id =%(station_id)s'''
get_station_parameter_filters_global = '''SELECT parameter.parameter_id,upper_boundary,lower_boundary,parameter.parameter FROM parameter INNER JOIN parameter_station_notification_filter ON parameter.parameter_id =parameter_station_notification_filter.parameter_id where station_id ='1' '''
insert_station_warnnings = '''INSERT INTO public.station_warnings(station_id, parameter_id, warning_time, value, margin_level, warning_status) VALUES ( %(station_id)s,%(parameter_id)s,%(time)s,%(value)s,%(margin_level)s, %(warning_status)s)'''

#query tpes
db_fetch = 'fetch'
db_insert = 'insert'
db_fetch_all = 'fetch_all'

#login types
log_debug = 'debugLog'
log_info = 'infoLog'
log_warning = 'warningLog'
log_error = 'errorLog'
log_critical = 'criticalLog'
log_duplicate = 'duplicateLog'

#data base credentials
DB_host = config('pg_db_host', default='localhost')
DB_database ='curw_IoT'
DB_password = config('pg_db_password',default ='postgress')
DB_port = config('pg_db_port',default='5432')
DB_user = config('pg_db_user',default='postgres')

#Encryption key
encryption_key=config('encryption_key', default = b'this is the secret key of the encryption')

#mongo DB Credentials
mongo_db_connection = config('mongo_db_connection',default='mongodb://root:example@localhost:27017')

#warnning levels
warning_exceed = 'exceed'
warning_below = 'below'
warning_normal = 'normal'