

import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("temp-humid-controller")
client.connect(mqttBroker)

# for temperature
tempSensorTopic = "326/temp"
tempControlTopic = "326/control/temp"

tempThreashold = 32
tempCanChange = 2

def on_message(client, userdata, message):
    print("Received " + str(message.payload.decode("utf-8")))
    if (float(message.payload.decode("utf-8")) < (tempThreashold - tempCanChange)):
        client.publish(tempControlTopic, "Provide Hot Air")
        print("published 'Provide Hot Air' to topic " + tempControlTopic)

    elif (float(message.payload.decode("utf-8")) > (tempThreashold + tempCanChange)):
        client.publish(tempControlTopic, "Provide Cold Air")
        print("published 'Provide Cold Air' to topic " + tempControlTopic)

    else:
        print("Maintainig current temperature levels")


def run():
    client.subscribe(tempSensorTopic)
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

