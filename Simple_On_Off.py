import paho.mqtt.client as mqtt
import time

# Replace with the appropriate values for your MQTT broker and smart plug
MQTT_BROKER = "your_mqtt_broker_address"
MQTT_PORT = 1883
MQTT_TOPIC = "your_smart_plug_topic"
MQTT_USERNAME = "your_username"
MQTT_PASSWORD = "your_password"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

# Turn the smart plug on
print("Turning the smart plug on")
client.publish(MQTT_TOPIC, "ON")
time.sleep(5)

# Turn the smart plug off
print("Turning the smart plug off")
client.publish(MQTT_TOPIC, "OFF")

time.sleep(5)

client.loop_stop()
client.disconnect()
