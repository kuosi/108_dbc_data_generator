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

print ("{\"messages\": [")

msg_size = len(db.messages)
msg_size_i = 1

for msg in db.messages:
    print ("{")
    print ("\"id\": " + str(msg.frame_id) + ",")
    print ("\"name\": \"" + msg.name + "\",")
    print ("\"is_extended_frame\": " + str(msg.is_extended_frame).lower() + ",")
    print ("\"length\": " + str(msg.length) + ",")
    print ("\"is_multiplexed\": " + str(msg.is_multiplexed()).lower()+ ",")
    
    print ("\"signals\": [")

    sig_size = len(msg.signals)
    sig_size_i = 1

    for sig in msg.signals:
        print ("{")
        #The signal name as a string.
        print ("\"name\": \"" + sig.name + "\",")
        #The start bit position of the signal within its message.
        print ("\"start\": " + str(sig.start) + ",")
        #The length of the signal in bits.
        print ("\"length\": " + str(sig.length) + ",")
        #Signal byte order as \"little_endian\" or \"big_endian\".
        print ("\"byte_order\": \"" + str(sig.byte_order) + "\",")
        #True if the signal is signed, False otherwise. Ignore this attribute if is_float is True.
        print ("\"is_signed\": " + str(sig.is_signed).lower() + ",")
        #True if the signal is a float, False otherwise.
        print ("\"is_float\": " + str(sig.is_float).lower() + ",")
        #The scale factor of the signal value.
        print ("\"scale\": " + str(sig.scale if sig.scale!=None else 1) + ",")
        #The offset of the signal value.
        print ("\"offset\": " + str(sig.offset if sig.offset!=None else 0) + ",")
        #The minimum value of the signal, or None if unavailable.
        print ("\"minimum\": " + str(sig.minimum if sig.minimum!=None else 0) + ",")
        #The maximum value of the signal, or None if unavailable.
        print ("\"maximum\": " + str(sig.maximum if sig.maximum!=None else 0) + ",")
        #The high precision values of scale, offset, minimum and maximum.
        print ("\"decimal_scale\": " + str(sig.decimal.scale if sig.decimal.scale!=None else 1) + ",")
        print ("\"decimal_offset\": " + str(sig.decimal.offset if sig.decimal.offset!=None else 0) + ",")
        print ("\"decimal_minimum\": " + str(sig.decimal.minimum if sig.decimal.minimum!=None else 0) + ",")
        print ("\"decimal_maximum\": " + str(sig.decimal.maximum if sig.decimal.maximum!=None else 0) + ",")
        #The unit of the signal as a string, or None if unavailable.
        if sig.unit == None:
            print ("\"unit\": \"\",")
        else:
            print ("\"unit\": \"" + str(sig.unit) + "\",")
        #A dictionary mapping signal values to enumerated choices, or None if unavailable.
        print ("\"choices\": {")
        if sig.choices != None:
            cho_size = len(sig.choices)
            cho_size_i = 1
            for key in sig.choices:
                if cho_size_i < cho_size:
                    print("\"" + str(key) + "\": " + "\"" + str(sig.choices[key]) + "\",")
                    cho_size_i = cho_size_i + 1
                else:
                    print("\"" + str(key) + "\": " + "\"" + str(sig.choices[key]) + "\"")                
        print ("},")
        #True if this is the multiplexer signal in a message, False otherwise.
        print ("\"is_multiplexer\": " + str(sig.is_multiplexer).lower() + ",")
        #The multiplexer ids list if the signal is part of a multiplexed message, None otherwise.
        #TODO: Can a signals have multiple multiplexer_ids?
        if sig.multiplexer_ids != None:
            print ("\"multiplexer_ids\": " + str(sig.multiplexer_ids) + ",")
        else:
            print ("\"multiplexer_ids\": [],")
        #The multiplexer signal if the signal is part of a multiplexed message, None otherwise.
        if sig.multiplexer_signal != None:
            print ("\"multiplexer_signal\": \"" + str(sig.multiplexer_signal) + "\"")
        else:
            print ("\"multiplexer_signal\": \"\"")
        
        if sig_size_i < sig_size:
            print ("},")
            sig_size_i = sig_size_i + 1
        else:
            print ("}")

    print ("]")

    if msg_size_i < msg_size:
        print ("},")
        msg_size_i = msg_size_i + 1
    else:
        print ("}")

print ("]}")