#!/usr/bin/env python

import cantools
import json
import can
import random
import math
from time import sleep
import os

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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

for msg in data:
    message = db.get_message_by_name(msg)
    
    signals_dict = {}

    for signal in message.signals:
        #if not (is_number(str(signal.minimum)) and is_number(str(signal.maximum))):
        #print (str(message.name) + "." + str(signal.name) + " " + str(signal.minimum) + " " + str(signal.maximum))
        print (str(signal.scale) + "  ---  " + str(signal.offset) + "  +++  " + str(signal.minimum) + " " + str(signal.maximum))

        '''print ("\"choices\": {")
        if signal.choices != None:
            cho_size = len(signal.choices)
            cho_size_i = 1
            for key in signal.choices:
                if cho_size_i < cho_size:
                    print("\"" + str(key) + "\": " + "\"" + str(signal.choices[key]) + "\",")
                    cho_size_i = cho_size_i + 1
                else:
                    print("\"" + str(key) + "\": " + "\"" + str(signal.choices[key]) + "\"")                
        print ("},")'''

        