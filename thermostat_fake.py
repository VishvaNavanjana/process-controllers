import paho.mqtt.client as mqtt
import random
import time

mqttBroker = "mqtt.eclipseprojects.io"
client =mqtt.Client("Thermostat")
client.connect(mqttBroker)

topic = "326/temp"

while True:
    temperature = random.uniform(0, 100)
    client.publish(topic, temperature)
    print("published " + str(temperature) + "to topic " + topic)
    time.sleep(5)

