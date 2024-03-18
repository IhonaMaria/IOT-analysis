
import json
from paho.mqtt import client as mqtt
from functions import check_temperature, convert_temperature

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    client.subscribe("temp_sensor/filter") # Subscribes to the topic that contains the raw data, the functions and the functions parameter's

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    temperature = payload['rawData']['temperature']
    actions = payload['actions']
    
    for action in actions:
        function_name = action['function']
        args = action['args']
        
        # Map the function name to a real function call
        if function_name == "check_temperature":
            result = check_temperature(temperature,**args)
            message=f"Temperature check: {'above' if result else 'below'} threshold."
        elif function_name == "convert_temperature":
            result = convert_temperature(temperature, **args)
            message=f"Converted Temperature: {result}"
        else:
             message = "Unknown function requested."

        print(message)
        # Publish the result or message back to MQTT
        client.publish("temp_sensor/results", message)



clientId = 'TemperatureActionExecutor'
broker = 'iot.jlm.local'

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, clientId)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker, 1883)
    client.loop_forever()

except KeyboardInterrupt:
        print("Script stopped by the user")

# Stop the loop and disconnect 
client.loop_stop()
client.disconnect()


