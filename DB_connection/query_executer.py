#Database Connection
import logging
from os import execlp
import psycopg2
import psycopg2.extras
import time

#import logger 
import Login.loger as logger
#configurations
import Configurations.config as config


def execute_query( sql_query=None,params=None,query_type ='fetch',query_reason=None):

    connection= None # database connection object
    time_start = time.time()
    try:
        connection = psycopg2.connect(host=config.DB_host,
                                        database= config.DB_database,
                                        user=config.DB_user,
                                        password=config.DB_password,
                                        port=config.DB_port,
                                        )
        try:
            #get data from database
            if(query_type ==config.db_fetch):
                cursor=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(sql_query,params)
                result = cursor.fetchall()
                if result == []:
                    connection.close()
                    return None
                else:
                    result= dict(result[0])
                    connection.close()
                    #data fetch success 
                    time_now = time.time()
                    #login the success record
                    logger.log(log_type=config.log_info,params=str(query_reason)+"-Success-Durtaion:"+str(time_now-time_start)+"Query type -"+str(config.db_fetch))
                    return result
            #insert or upsert quaries
            if(query_type == config.db_insert):
                cursor=connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(sql_query,params)
                result=connection.commit()
                connection.close()
                #data fetch success 
                time_now = time.time()
                #login the success record
                logger.log(log_type=config.log_info,params=str(query_reason)+"-Success-Durtaion:"+str(time_now-time_start)+"Query type -"+str(config.db_insert))
                return result
            if(query_type == config.db_fetch_all):
                cursor=connection.cursor()
                cursor.execute(sql_query,params)
                columns = list(cursor.description)
                result=cursor.fetchall()
                results = []
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col.name] = row[i]
                    results.append(row_dict)
                
                return results
        #error in the key
        except KeyError as e:
            logger.log(log_type=config.log_error,params=e)
            print("Key Error",e)

    # error in the database connection
    except (Exception,psycopg2.DatabaseError) as e:
        logger.log(log_type=config.log_critical,params=e)
        print("Database Error", e)



    