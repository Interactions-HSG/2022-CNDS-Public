#!/usr/bin/python3

import os, sys, logging, time
import requests, struct, json
from base64 import b64decode,b64encode
from datetime import datetime,timezone
import paho.mqtt.client as mqtt
from datetime import datetime
from yawigle import client

## Import local config
from config import *

# Functions
iso2ts   = lambda iso: datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc).timestamp()
hwid2eui = lambda hwid: '-'.join(hwid[2*i:2*i+2] for i in range(8))

# --- TTN FUNCTIONS --------------------------

def on_connect(mqttc, obj, flags, rc):
    print("\nConnected to " + str(TTN_URL))

def on_message(mqttc, obj, msg):
    try: 
        print("\nMessage: " + msg.topic + " " + str(msg.qos)) # + " " + str(msg.payload))
        parsedJSON = json.loads(msg.payload)
        # Uncomment this to fill your terminal screen with JSON
        # print(json.dumps(parsedJSON, indent=4))	
        if(parsedJSON["uplink_message"] is not None):
            payload = b64decode(parsedJSON["uplink_message"]["frm_payload"]).hex() 
            deveui = hwid2eui(parsedJSON["end_device_ids"]["dev_eui"])
            print("Payload: {}".format(payload))
            dmsmsg = json.dumps({
            deveui: {
                "fcnt":       parsedJSON["uplink_message"]["f_cnt"],
                "port":       parsedJSON["uplink_message"]["f_port"],
                "payload":    payload,
                "dr":         0,
                "freq":       int(parsedJSON["uplink_message"]["settings"]["frequency"]),
                "timestamp":  iso2ts(parsedJSON["uplink_message"]["settings"]["time"][:26])
            }
            })
            
    except Exception as e: 
        print("Error processing message: {}".format(e))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("\nSubscribed to " + str(MQTT_TOPIC))

def on_log(mqttc, obj, level, string):
    print("\nLog: "+ string)
    logging_level = mqtt.LOGGING_LEVEL[level]
    logging.log(logging_level, string)


# --- MAIN --------------------------
print(os.path.basename(__file__) + " " + VER)

# Init mqtt client
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
#mqttc.on_log = on_log		# Logging for debugging OK, waste

# Connecting to TTN
# Setup authentication from settings above
mqttc.username_pw_set(User, Password)
# IMPORTANT - this enables the encryption of messages
mqttc.tls_set()	# default certification authority of the system
#mqttc.tls_set(ca_certs="mqtt-ca.pem") # Use this if you get security errors
# It loads the TTI security certificate. Download it from their website from this page: 
# https://www.thethingsnetwork.org/docs/applications/mqtt/api/index.html
# This is normally required if you are running the script on Windows
mqttc.connect(TTN_URL, 8883, 60)
mqttc.subscribe(MQTT_TOPIC, 0)	# all device uplinks

print("Waiting for Data")
try:    
	run = True
	while run:
		mqttc.loop(10) 	# seconds timeout / blocking time
		print(".", end="", flush=True)	# feedback to the user that something is actually happening
    
except KeyboardInterrupt:
    print("Exit")
    sys.exit(0)