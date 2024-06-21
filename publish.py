# importing libraries
import paho.mqtt.client as paho
import os
import ssl
import random
import string
import json
from time import sleep
from random import uniform

connflag = False

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))

def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic + " " + str(msg.payload))

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

def getMAC(interface='eth0'):
    # Return the MAC address of the specified interface
    try:
        mac = open('/sys/class/net/%s/address' % interface).read()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]

def getEthName():
    # Get name of the Ethernet interface
    try:
        for root, dirs, files in os.walk('/sys/class/net'):
            for dir in dirs:
                if dir[:3] == 'enx' or dir[:3] == 'eth':
                    return dir
    except:
        return "None"

mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func

#### Change following parameters ####
awshost = "XXXXXXXXXamazonaws.com"  # Endpoint
awsport = 8883                                              # Port no.
clientId = "MLC_NEW_Client"                                 # Thing_Name
thingName = "MLC_NEW_Client"                                # Thing_Name
caPath = "/home/MLC/Downloads/AmazonRootCA1.pem"       # Root_CA_Certificate_Name
certPath = "/home/MLC/Downloads/XXXXXXXX-certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "/home/MLC/Downloads/XXXXXXX-private.pem.key"      # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server

mqttc.loop_start()                                          # Start the loop

while True:
    sleep(5)
    if connflag:
        ethName = getEthName()
        ethMAC = getMAC(ethName)
        macIdStr = ethMAC
        randomNumber = uniform(20.0, 25.0)
        random_string = get_random_string(8)
        payload = {
            "mac_Id": macIdStr,
            "random_number": randomNumber,
            "random_string": random_string
        }
        payload_json = json.dumps(payload)
        mqttc.publish("MLC", payload_json, qos=1)  # topic: # Publishing  values
        print("msg sent: ElectronicsInnovation")  # Print sent  msg on console
        print(payload_json)
    else:
        print("waiting for connection...")
