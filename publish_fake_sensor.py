from paho.mqtt import client as mqtt
import time
import random

# Fake temperature data generator for range 20 to 40 degrees
def generate_temperature_data():
    return round(random.uniform(20.0, 40.0), 2)


def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")

def publish_temperature_data(client):
    while True:  # Infinite loop to continuously publish data
        temperature = generate_temperature_data()
        client.publish("temp_sensor/data", str(temperature))  
        print(f"Published temperature: {temperature}")
        time.sleep(5)  # Wait for 5 seconds before the next publish

clientId = 'Ihona'
port = 1883
broker = 'iot.jlm.local'

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, clientId)

# Assign the on_connect callback function
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker, port)

# Start the loop in a separate thread
client.loop_start()

try:
    publish_temperature_data(client)
except KeyboardInterrupt:
    print("Script stopped by the user")

# Stop the loop and disconnect 
client.loop_stop()
client.disconnect()
