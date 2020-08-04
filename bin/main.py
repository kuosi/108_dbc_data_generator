#!/usr/bin/env python

import cantools
import json
import can
import random
import math
from time import sleep
import os

#snap_data_dir = os.environ.get('SNAP_DATA')
snap_data_dir = "../base"

f = open(snap_data_dir + '/options/configuration.json')
config = json.load(f)
f.close()

can_interface = config["can"]["interface"]
can_fd = True if (config["can"]["fd"].strip().lower() == "true") else False
can_frequency_hz = config["can"]["frequency"]
can_frequency_s = (1000 / can_frequency_hz) / 1000
dbc_file = config["dbc"]["file"]
dbc_messages = config["dbc"]["messages"]

db = cantools.database.load_file(dbc_file)

f = open(dbc_messages)
data = f.readlines()
f.close()
data = [x.strip() for x in data]

can_bus = can.interfaces.socketcan.SocketcanBus(can_interface, fd=can_fd)

while True:
    sleep(can_frequency_s)
    for msg in data:
        message = db.get_message_by_name(msg)
        
        if (can_fd or ((not can_fd) and message.length<=8)):

            signals_dict = {}

            for signal in message.signals:

                if signal.choices!=None:
                    random_val_int = random.randint(1, len(signal.choices))
                    i = 1
                    choosen_key = ""
                    for key in signal.choices:
                        if (i == random_val_int):
                            choosen_key = key
                        i = i+1
                    random_val = int(choosen_key)

                    signals_dict[str(signal.name)] = random_val
                else:
                    min = signal.minimum if signal.minimum!=None else 0
                    max = signal.maximum if signal.maximum!=None else 0

                    new_min = (min - signal.offset) / signal.scale
                    new_max = (max - signal.offset) / signal.scale
                    random_val_int = random.randint(int(new_min), int(new_max))

                    random_val = (random_val_int * signal.scale) + signal.offset

                    signals_dict[str(signal.name)] = random_val

                    if (random_val < min or random_val > max):
                        print (signal.name)
                        print ("Min: " + str(min) + " -- Max: " + str(max) + " -- New_Min: " + str(new_min) + " -- New_Max: " + str(new_max))
                        print ("random_val_int: " + str(random_val_int) + " -- random_val: " + str(random_val))
                        break


                
                
                '''if not (str(random_val).isdigit()):
                    print (signal.name)
                    print (random_val)'''

            try:
                can_message = can.Message(arbitration_id=message.frame_id, data=message.encode(signals_dict), is_fd=can_fd)
                can_bus.send(can_message)
            except Exception as e: # work on python 2.x
                print ("######")
                print(str(e))
                print ("######")
                print (message)
                print (signals_dict)
                '''print (can_message)
                print (can_message.arbitration_id)
                print (message.frame_id)'''
