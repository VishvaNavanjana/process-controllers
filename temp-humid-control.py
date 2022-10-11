

import paho.mqtt.client as mqtt
import json
import datetime

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("temp-humid-controller")
# client.connect(mqttBroker)

# for temperature
tempSensorTopic = "326project/smartbuilding/hvac/sensor/temperature/zoneX/"
tempControlTopic = "326project/smartbuilding/hvac/control/boiler/"
tempThreashold = 32
tempCanChange = 2

# for humidity
humidSensorTopic = "326project/smartbuilding/hvac/sensor/humidity/zoneX/"
humidControlTopic = "326project/smartbuilding/hvac/control/chiller/"
humidThreashold = 65
humidCanChange = 2

# controlling temperature
def on_message_for_temp(client, userdata, message):
    data = json.loads(message.payload)
    print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return

    temperature = values[1]
    print("Received Temperature " + str(temperature))

    if (temperature < (tempThreashold - tempCanChange)):

        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
        }
        client.publish(tempControlTopic, json.dumps(x))
        print("published 'Provide Hot Air' to topic " + tempControlTopic)

    elif (temperature > (tempThreashold + tempCanChange)):

        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
        }
        client.publish(tempControlTopic, json.dumps(x))
        print("published 'Provide Cold Air' to topic " + tempControlTopic)

    else:
        client.publish(tempControlTopic, "Turn OFF")
        print("Maintainig current temperature levels")

    print()


# controlling humidity
def on_message_for_humid(client, userdata, message):

    data = json.loads(message.payload)
    print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'humid'):
        return

    humidity = values[1]

    print("Received Humidity " + str(humidity))

    if (humidity < (humidThreashold - humidCanChange)):
        client.publish(tempControlTopic, "Provide Hot Air")
        print("published 'Increase Humidity' to topic " + humidControlTopic)

    elif (humidity > (tempThreashold + tempCanChange)):
        client.publish(tempControlTopic, "Provide Cold Air")
        print("published 'Decrease Humidity' to topic " + humidControlTopic)

    else:
        client.publish(humidControlTopic, "Turn OFF")
        print("Maintainig current Humidity levels")

    print()


#
client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(humidSensorTopic, on_message_for_humid)
client.connect("vpn.ce.pdn.ac.lk", port=8883)
client.subscribe([("326project/smartbuilding/hvac/sensor/temperature/zoneX/", 0), ("326project/smartbuilding/hvac/sensor/humidity/zoneX/", 0)])
client.loop_forever()
#








