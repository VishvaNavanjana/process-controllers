

import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("temp-humid-controller")
# client.connect(mqttBroker)

# for temperature
tempSensorTopic = "326/sensor/temp"
tempControlTopic = "326/control/temp"
tempThreashold = 32
tempCanChange = 2

# for humidity
humidSensorTopic = "326/sensor/humidity"
humidControlTopic = "326/control/humidity"
humidThreashold = 65
humidCanChange = 2

# controlling temperature
def on_message_for_temp(client, userdata, message):
    print("Received Temperature " + str(message.payload.decode("utf-8")))

    if (float(message.payload.decode("utf-8")) < (tempThreashold - tempCanChange)):
        client.publish(tempControlTopic, "Provide Hot Air")
        print("published 'Provide Hot Air' to topic " + tempControlTopic)

    elif (float(message.payload.decode("utf-8")) > (tempThreashold + tempCanChange)):
        client.publish(tempControlTopic, "Provide Cold Air")
        print("published 'Provide Cold Air' to topic " + tempControlTopic)

    else:
        client.publish(tempControlTopic, "Turn OFF")
        print("Maintainig current temperature levels")

# controlling humidity
def on_message_for_humid(client, userdata, message):
    print("Received Humidity " + str(message.payload.decode("utf-8")))

    if (float(message.payload.decode("utf-8")) < (humidThreashold - humidCanChange)):
        client.publish(tempControlTopic, "Provide Hot Air")
        print("published 'Increase Humidity' to topic " + humidControlTopic)

    elif (float(message.payload.decode("utf-8")) > (tempThreashold + tempCanChange)):
        client.publish(tempControlTopic, "Provide Cold Air")
        print("published 'Decrease Humidity' to topic " + humidControlTopic)

    else:
        client.publish(humidControlTopic, "Turn OFF")
        print("Maintainig current Humidity levels")




# client.message_callback_add(tempSensorTopic, on_message_for_temp)
# client.connect(mqttBroker)
# client.subscribe(tempSensorTopic)
# client.loop_forever()
#
# client.message_callback_add(humidSensorTopic, on_message_for_humid)
# client.connect(mqttBroker)
# client.subscribe(humidSensorTopic)
# client.loop_forever()


# def on_message(client, uerdata, message):
#     print(message.topic + " " + str(message.qos) + " " + str(message.payload))
#     print()
#
client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(humidSensorTopic, on_message_for_humid)
client.connect(mqttBroker)
client.subscribe("326/sensor/#")
client.loop_forever()
#
# client.loop_forever()


# def run():
#     client.subscribe(tempSensorTopic)
#     client.on_message = on_message_for_temp
#     time.sleep(5)
#     client.subscribe(humidSensorTopic)
#     client.on_message = on_message_for_humid
#     time.sleep(5)
#     client.loop_forever()
#
# run()


# def run():
#     client.subscribe(tempSensorTopic, 2)
#     client.subscribe(humidSensorTopic, 2)
#     client.message_callback_add(tempSensorTopic, on_message_for_temp)
#     # time.sleep(5)
#     client.message_callback_add(humidSensorTopic, on_message_for_humid)
#     # time.sleep(5)
#     # client.on_message = on_message
#
#     time.sleep(5)
#     client.loop_forever()
#
# run()







