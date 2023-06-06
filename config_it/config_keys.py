import sys
# import constant
# sys.path.append(constant.CONFIG)
from logger import logging
from except_error import soft_error

from config_it.connect_est import connect_config


class config_value:

    def __init__(self) -> None:
        pass 


    def value_input(self,database_name,collection_name,dict_values):

        try:

            connect=connect_config()
            collection=connect.mongodb_config(database_name,collection_name)
            collection.insert_one(dict_values)
            logging.info('value has been inserted')

        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)



    def value_retrieve(self,database_name,collection_name,value):

        try:

            connect=connect_config()
            collection=connect.mongodb_config(database_name,collection_name)
            val=collection.find_one(value)
            logging.info('value has been exctracted')
            
            return val

        except Exception as e:
            logging.info(soft_error(e,sys))
            raise soft_error(e,sys)

    
        

