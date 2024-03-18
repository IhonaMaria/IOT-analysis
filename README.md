# IOT-analysis

## Introduction
In simple terms, The Internet of Things, or IoT, is a system of interrelated computing devices that can collect and transfer data over a wireless network without human input. These devices can range from everyday objects to complex industrial machines.
Picture this: you’re away from home, but with just a few taps on your smartphone, you can illuminate your living space and adjust the temperature to create a comfortable atmosphere for when you return. What may seem like magic is made possible by MQTT – a messaging protocol used in many IoT applications. MQTT is a messaging protocol that enables communication between devices. It operates on a publish-subscribe model which allows devices to send messages on specific topics, while other devices can subscribe to those topics to receive the messages. 

## Objectives
This repository presents a workflow to process IoT sensor data in a modular and more automated way. 
We will simulate a temperature sensor that publishes sensor data every 5 seconds to the MQTT broker. Node-RED, which is a visual programming tool, will subscribe to that topic and publish to the broker a new topic with the specified function and arguments to apply.
A Python code is subscribed to that topic published by Node-RED and uses the provided information to process the temperature data by applying the desired functions. Finally, the processed information gets published and anyone can subscribe to that topic and access the final data. 

It seems very convoluted so far...But stay with me and you will see how everything makes more sense!

## Step 0 : Defining the processing functions
First of all, we create a python file named **"functions.py"** that contains two functions we wish to apply to the temperature sensor data. 
- The function check_temperature(data, threshold) checks if the temperature data exceeds a given threshold. If it does, it returns True. Otherwise, it returns False. The user must to specify the threshold desired. 
- The function convert_temperature(data, conversion) converts the temperature data into Farenheit, Kelvin or Celsius. The user must specify either 'fahrenheit', 'kelvin' or 'celsius' (if it selects Celcius, no conversion will be applied since the data is already in Celsius). 

This file is a starting point, any function can be added easily.

## Step 1: Publishing sensor data
We will be using the Python paho.mqtt library, which is a library that enables us to establish a connection to an MQTT broker and publish and subscribe to messages.
The Python code **"publish_fake_sensor.py"** connects to the broker (which it is hosted in a server with a specific port) and publishes fake temperature data (simulating a sensor) every 5 seconds. The values are obtained randomly and they can be between 20 and 40 Celsius degrees. The raw temperature data is published under the topic **temp_sensor/data**. 


![image](https://github.com/IhonaMaria/IOT-analysis/assets/119692820/fd561e13-35e3-4664-b22b-49351c31411a)

## Step 2: Subscribing with Node-RED
Node-RED is a flow-based, low-code development tool for visual programming, whose runtime is built on Node.js. Each node within a flow performs a unique and specific task. When data is transmitted to a node, the node processes it according to its designated function, before passing it on to the subsequent node in the flow. This system allows for the controlled execution and regulation of a wide range of operations, offering significant flexibility in creating real-time applications.

We create an mqtt out node that subscribes to the **temp_sensor/data** topic and a mqtt in node that recieves this data and passes it to a function node. This function node is a JavaScript function (**"javascript_function.js"**) that contains the desired function to apply to the raw temperature data and the arguments this function needs. In this way, users have the flexibility of changing the functions they want to use to process the data and the value of the arguments at any time with a few clicks. 

For example, through this function, the user can specify that he wants to apply the check_temperature function with a threshold to 30 to the data. It is important that the functions and arguments are correcly specified and exist in the **"functions.py"** file.
The Javascript function is then connected to an mqtt out node that publishes the raw temperature data together with the function specifications in json format in this topic: **temp_sensor/filter**

Here is the Node-RED workflow:

![image](https://github.com/IhonaMaria/IOT-analysis/assets/119692820/ea1feca4-b994-484f-a447-e61876d97903)

The debug node can be used to see the output messages of function 4. This is what the debug node prints for every message that arrives:

![image](https://github.com/IhonaMaria/IOT-analysis/assets/119692820/98bd1eb9-6f47-4a4d-8c7c-1cf5f54202d4)


## Step 3: Subscribing and publishing processed data
A Python code named **"filtering_modular.py"** imports the python functions from the functions file and subscribes to the topic **temp_sensor/filter**. Then, we use the on_message function from the paho.mqtt library to extract the information from the json message and apply the functions. 

This is what the processed message looks like:

![image](https://github.com/IhonaMaria/IOT-analysis/assets/119692820/a4f2de9e-1656-446a-b901-06e36eb44246)

We can see that the two functions are being executed correcly. We have modified the on_message function to obtain an "above threshold" message when the result of the check_temperature is True, and a message that says "below threshold" otherwise. Also, we can see the converted temperature as specified in the Javascript function with the respective units. 

These results are then published back to the MQTT broker under the topic: **temp_sensor/results**

## Step 4: Check the IoT workflow
We can use the MQTT explorer, which provides a structured and visual overview of the MQTT topics and the messages:

![image](https://github.com/IhonaMaria/IOT-analysis/assets/119692820/d41c3f49-00a2-42bb-a081-ef0af8dd3003)

We can see that, under the topic temp_sensor, there are 3 subtopics: data, filter and results. We can also see one example message of each subtopic. 
- Data subtopic has the raw temperature sensor data
- Filter subtopic has the payload message that Node-RED publishes which contains the raw data and the actions (function and arguments). In this case, the user decided to apply the check_temperature function with a threshold of 30, and the convert_temperature function with the argument kelvin. Obviously, this can be easily modified at anytime by the user based on his preferences. Maybe the user wants to add a new function that performs some calculations to the temperature data? Maybe he wants to change the threshold? Maybe he just wants to apply the convert_temperature function? This workflow gives the user this kind of flexibility.
- Result subtopic gives the results from applying the python functions. 
  
