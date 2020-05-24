#!/usr/bin/env python

import cantools
import json
import can
import random
import math
from time import sleep
import os

snap_data_dir = os.environ.get('SNAP_DATA')
#snap_data_dir = "../base"

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
                signals_dict[str(signal.name)] = random.randint(math.ceil(signal.minimum), math.floor(signal.maximum))
                if (signals_dict[str(signal.name)] < int(signal.minimum)) or (signals_dict[str(signal.name)] > int(signal.maximum)):
                    print (signals_dict[str(signal.name)])
                    print (int(signal.minimum))
                    print (int(signal.maximum))

            try:
                can_message = can.Message(arbitration_id=message.frame_id, data=message.encode(signals_dict), is_fd=can_fd)
                can_bus.send(can_message)
            except:
                print ("######")
                print (message)
                print (signals_dict)
                print (can_message)
                print (can_message.arbitration_id)
                print (message.frame_id)
