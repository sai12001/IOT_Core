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
awshost = "a2rvthmp83bq7x-ats.iot.ap-south-1.amazonaws.com" # Updated Endpoint
awsport = 8883                                              # Port number
clientId = "MLC_NEW_Client"                                 # Thing Name
thingName = "MLC_NEW_Client"                                # Thing Name
caPath = "/home/maintwiz/Downloads/AmazonRootCA1.pem"       # Updated Root CA Certificate
certPath = "/home/maintwiz/Downloads/546afbc27b03f066d1bfbbaca27dc36c3cce20b629cef85e74308ce8c9a9eed5-certificate.pem.crt" # Updated Certificate
keyPath = "/home/maintwiz/Downloads/546afbc27b03f066d1bfbbaca27dc36c3cce20b629cef85e74308ce8c9a9eed5-private.pem.key"      # Updated Private Key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)               # Connect to AWS server

mqttc.loop_forever()                                        # Start receiving in loop
