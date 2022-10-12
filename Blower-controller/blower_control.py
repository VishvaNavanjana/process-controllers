

import paho.mqtt.client as mqtt
import json
import datetime

client = mqtt.Client("blower-controller")
# client.connect(mqttBroker)

# for temperature
tempSensorTopic = "326project/smartbuilding/hvac/sensor/temperature/floorX/roomX"
# tempControlTopic = "326project/smartbuilding/hvac/control/boiler/"
tempThreashold = 32
tempCanChange = 2

# for humidity
humidSensorTopic = "326project/smartbuilding/hvac/sensor/humidity/floorX/roomX"
# humidControlTopic = "326project/smartbuilding/hvac/control/chiller/"
humidThreashold = 65
humidCanChange = 2

tempPrevious = 28 # default value
humidityPrevious = 45 # default value

blowerControlTopic = "control/blower"


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

    tempPrevious = values[1]

    create_blower_control_command(tempPrevious, humidityPrevious)

    #
    #
    # print("Received Temperature " + str(temperature))
    #
    # if (temperature < (tempThreashold - tempCanChange)):
    #
    #     x = {
    #         "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    #         "state": 1
    #     }
    #     client.publish(tempControlTopic, json.dumps(x))
    #     print("published 'Provide Hot Air' to topic " + tempControlTopic)
    #
    # elif (temperature > (tempThreashold + tempCanChange)):
    #
    #     x = {
    #         "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    #         "state": 0
    #     }
    #     client.publish(tempControlTopic, json.dumps(x))
    #     print("published 'Provide Cold Air' to topic " + tempControlTopic)
    #
    # else:
    #     client.publish(tempControlTopic, "Turn OFF")
    #     print("Maintainig current temperature levels")
    #
    # print()


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

    humidityPrevious = values[1]

    create_blower_control_command(tempPrevious, humidityPrevious)

    # print("Received Humidity " + str(humidity))
    #
    # if (humidity < (humidThreashold - humidCanChange)):
    #
    #     x = {
    #         "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    #         "state": 1
    #     }
    #     client.publish(tempControlTopic, json.dumps(x))
    #     print("published 'Increase Humidity' to topic " + humidControlTopic)
    #
    # elif (humidity > (tempThreashold + tempCanChange)):
    #
    #     x = {
    #         "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    #         "state": 0
    #     }
    #     client.publish(tempControlTopic, json.dumps(x))
    #     print("published 'Decrease Humidity' to topic " + humidControlTopic)
    #
    # else:
    #     client.publish(humidControlTopic, "Turn OFF")
    #     print("Maintainig current Humidity levels")
    #
    # print()

def create_blower_control_command(temp, humid):

    # x = {
    #     "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    #     "speed": 0.5
    # }
    # client.publish(blowerControlTopic, json.dumps(x))
    # print("published 'Provide Hot Air' to topic " + blowerControlTopic)
    #
    # print()


    # if temp and humid are higher
    if ((tempThreashold+tempCanChange) < temp):
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": 0.5
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Increase fan speed ' to topic " + blowerControlTopic)

    # if temp and humid are lower
    elif ((tempThreashold-tempCanChange) > temp):
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": -0.5
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Decrease fan speed ' to topic " + blowerControlTopic)

    # otherwise no change
    else:
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": 0
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Don't change fan speed ' to topic " + blowerControlTopic)

    print()


#
client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(humidSensorTopic, on_message_for_humid)
client.connect("vpn.ce.pdn.ac.lk", port=8883)
client.subscribe([("326project/smartbuilding/hvac/sensor/temperature/floorX/roomX", 0), ("326project/smartbuilding/hvac/sensor/humidity/floorX/roomX", 0)])
client.loop_forever()
#








