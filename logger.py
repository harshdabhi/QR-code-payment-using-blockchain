import logging
import os
import datetime



def logger():
    os.mkdir('./log_file'+datetime.datetime.now().strftime(),exist_ok=True)
    pass
'''
can code logging as per requirements
'''
    
