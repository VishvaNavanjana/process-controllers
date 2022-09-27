import paho.mqtt.client as mqtt
import random
import time

mqttBroker = "mqtt.eclipseprojects.io"
client =mqtt.Client("Thermostat")
# client.connect(mqttBroker)

topic = "326/sensor/humidity"

while True:
    client.connect(mqttBroker)
    humidity = random.uniform(0, 100)
    client.publish(topic, humidity)
    print("published " + str(humidity) + "to topic " + topic)
    time.sleep(5)

