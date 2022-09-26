

import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("temp-humid-controller")
client.connect(mqttBroker)

tempTopic = "326/temp"

def on_message(client, userdata, message):
    print("Received " + str(message.payload.decode("utf-8")))

def run():
    client.subscribe(tempTopic)
    client.on_message = on_message
    time.sleep(1)
    client.loop_forever()

run()


# client.loop_start()
# client.subscribe(tempTopic)
# client.on_message = on_message
# time.sleep(1)
# client.loop_end()



# get data from the thermostat and humidity sensor (todo)

# validate data



# check temp

# check humidity

# send data

