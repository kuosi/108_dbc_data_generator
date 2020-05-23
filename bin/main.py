#!/usr/bin/env python

import cantools
import json
import can
import numpy.random as random2
import random
import math
from time import sleep
import os

snap_data_dir = os.environ.get('SNAP_DATA')
#snap_data_dir = "../base"


def bounded_random(min, max):
    mu = (min + max)/2
    sigma = abs((mu-min)/3)
    value = int(random2.normal(mu, sigma))
    while value < min or value > max:
        value = int(random2.normal(mu, sigma))
    return value

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
        #print(hex(message.frame_id).upper().replace("0X", ""))

        if (can_fd or ((not can_fd) and message.length<=8)):

            signals_dict = {}

            for signal in message.signals:
                #signals_dict[str(signal.name)] = random.randint(math.ceil(int(signal.minimum)), math.floor(int(signal.maximum)))
                signals_dict[str(signal.name)] = bounded_random(signal.minimum, signal.maximum)
                if (signals_dict[str(signal.name)] < int(signal.minimum)) or (signals_dict[str(signal.name)] > int(signal.maximum)):
                    print (signals_dict[str(signal.name)])
                    print (int(signal.minimum))
                    print (int(signal.maximum))
                

            #print (signals_dict)

            try:
                can_message = can.Message(arbitration_id=int(message.frame_id), data=message.encode(signals_dict), is_fd=can_fd)
                can_bus.send(can_message)
            except:
                print ("######")
                print (message)
                print (signals_dict)
                print (can_message)
                print (can_message.arbitration_id)
                print (message.frame_id)