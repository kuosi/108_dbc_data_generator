#!/usr/bin/env python3

import cantools
import json
import can
import random
import math
from time import sleep
import os
import sys
import argparse
import logging
from datetime import datetime

'''
Check if a value can be represented with bit lenght of a signal.
value: value to be checked. This is the real value
signal: signal to be checked
'''
def check_value(value, signal):
    #Maximum value that can be represented by the signal
    max_bit = pow(2, signal.length) - 1
    
    #Remove offset and downscale
    val_bit = (value - signal.offset) / signal.scale
    
    #If the value can not be represented in the signal, return the maximum value that can be represented
    if val_bit > max_bit:
        value = (max_bit * signal.scale) + signal.offset
    
    return value

def main(argv):
    
    #Get the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configfile', required=True, help="Configuration file")
    parser.add_argument('-b', '--dbcfile', required=True, help="DBC file")

    args = parser.parse_args()

    configfile = args.configfile
    dbcfile = args.dbcfile
    
    #Load the configuration file
    f = open(configfile)
    config = json.load(f)
    f.close()

    #Configurations
    can_interface = config["can"]["interface"] #Configured can interface where the generated can data shall be sent
    can_fd = True if (config["can"]["fd"].strip().lower() == "true") else False #True if can message with size <= 64 Bytes shall be sent. Shall match with the CAN interface.
    default_sending_cycle_time= config["cycle_time"]["sending"] #Default cycle time in ms
    dbc_messages = config["dbc"]["MsgNames"] #Semi-column separated CAN Message Names
    logging_level = config["logging"]["level"] #Debug level

    #Load the dbc file
    db = cantools.database.load_file(dbcfile)

    
    '''#In case we want to generate all IDs of the dbc
    for msg in db.messages:
        print (str(msg.frame_id))'''

    #set logging
    log_level={
      'debug':logging.DEBUG,
      'info':logging.INFO,
      'warning':logging.WARNING,
      'error':logging.ERROR,
      'critical':logging.CRITICAL
    }

    if (log_level[logging_level]):
      logging.basicConfig(level=log_level[logging_level])
    else:
      logging.basicConfig(level=logging.DEBUG)

    logging.info('Configuration file: "' + configfile)
    logging.info('DBC file: "' + dbcfile)
    
    #Get selected message IDs
    data = dbc_messages.split(';')
    data = [x.strip() for x in data]
    print(data)

    dict_last_send = {}

    #Connect to the can interface
    can_bus = can.interfaces.socketcan.SocketcanBus(can_interface, fd=can_fd)

    #Start generating and sending messages
    while True:
        
        #sleep(0.1) #Sleep for 10 ms

        for msg_name in data:
            
            #Get one of the selected dbc messages
            message = db.get_message_by_name(msg_name)

            #Only consider can messages of max size 8 bytes in case of normal CAN or max size 64 bytes in case of CAN FD.
            if ((can_fd and message.length <= 64) or ((not can_fd) and message.length <= 8)):

                timestamp = datetime.now().timestamp() * 1000

                #get the cycle time
                sending_cycle = default_sending_cycle_time if message.cycle_time <= 0 else message.cycle_time

                #Check if the message shall be sent
                send = False        
                if (not (message.name in dict_last_send)): #If the message has never been sent, then send
                    send = True
                else:
                    print(timestamp - dict_last_send[message.name])
                    if timestamp - dict_last_send[message.name] >= sending_cycle: #Check if the cycle time has already elapse since the last time
                        send = True
                    
                logging.debug('Message name: ' + message.name)
                logging.debug('Cycle Time: ' + str(sending_cycle))
                logging.debug('Decision: ' + 'Send!' if send else 'Do not send!')

                if send:
                    signals_dict = {}

                    for signal in message.signals:

                        #If the signal is a chice choose randomly a choice

                        min = signal.minimum if signal.minimum != None else 0
                        max = signal.maximum if signal.maximum != None else 0
                        
                        if signal.choices != None:
                            
                            random_val_int = random.randint(1, len(signal.choices))
                            i = 1
                            choosen_key = ""
                            for key in signal.choices:
                                if (i == random_val_int):
                                    choosen_key = key
                                i = i+1
                            random_val = int(choosen_key)

                        else:
                            #Generate a random value for the signal                    
                            random_val = random.randint(int(min), int(max))
                        
                        #Make sure that the generated value is between min and max
                        random_val = min if random_val < min else (
                            max if random_val > max else random_val)
                        #Make sure that the generated value can be represented by the signal
                        random_val = check_value(random_val, signal)

                        signals_dict[str(signal.name)] = random_val


                    try:
                        #Create and send can message
                        can_message = can.Message(
                            arbitration_id=message.frame_id, data=message.encode(signals_dict), is_fd=can_fd)
                        can_bus.send(can_message)
                        dict_last_send[message.name] = timestamp
                        logging.debug(str(timestamp) + " - " + message.name + " - " + str(can_message))
                    except Exception as e:
                        logging.debug(str(e))
                        logging.debug(message)
                        '''logging.debug(signals_dict)
                        logging.debug(can_message)
                        logging.debug(can_message.arbitration_id)
                        logging.debug(message.frame_id)'''


if __name__ == "__main__":
    main(sys.argv[1:])