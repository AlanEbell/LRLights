import paho.mqtt.client as mqtt
import time

# Enter the IP address of your Smart Plug 2
broker_address = "xxx.xxx.xxx.xxx"

# Enter the MQTT topics for controlling the Smart Plug 2
topic_on = "smartplug2/on"
topic_off = "smartplug2/off"

# Enter your MQTT username and password (if applicable)
username = ""
password = ""

# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

# Connect to the MQTT broker
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, 1883, 60)

# Turn the Smart Plug 2 on
client.publish(topic_on, payload="on", qos=0, retain=False)
time.sleep(1)

# Turn the Smart Plug 2 off
client.publish(topic_off, payload="off", qos=0, retain=False)
time.sleep(1)

# Disconnect from the MQTT broker
client.disconnect()
