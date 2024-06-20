# Importing libraries
import paho.mqtt.client as paho
import os
import ssl

def on_connect(client, userdata, flags, rc):                # Function for making connection
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("your/topic/here", 1)                  # Subscribe to the specified topic

def on_message(client, userdata, msg):                      # Function for receiving messages
    print("topic: " + msg.topic)
    print("payload: " + str(msg.payload))

mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # Assign on_connect function
mqttc.on_message = on_message                               # Assign on_message function

#### Change following parameters #### 
awshost = "XXXXXXXXXamazonaws.com"  # Endpoint
awsport = 8883                                              # Port no.
clientId = "MLC_NEW_Client"                                 # Thing_Name
thingName = "MLC_NEW_Client"                                # Thing_Name
caPath = "/home/maintwiz/Downloads/AmazonRootCA1.pem"       # Root_CA_Certificate_Name
certPath = "/home/maintwiz/Downloads/XXXXXXXX-certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "/home/maintwiz/Downloads/XXXXXXX-private.pem.key"      # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)               # Connect to AWS server

mqttc.loop_forever()                                        # Start receiving in loop
