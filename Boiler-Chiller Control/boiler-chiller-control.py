import paho.mqtt.client as mqtt
import json

mqttBroker = "vpn.ce.pdn.ac.lk"
client = mqtt.Client("boiler-chiller-controller")

#temperature at cold air duct
tempColdAirSensorTopic = "326/sensor/coldairduct"
tempColdAirControlTopic = "326/control/coldairduct"
tempColdAirThreashold = 25

#temparature at hot air duct
tempHotAirSensorTopic = "326/sensor/hotairduct"
tempHotAirControlTopic = "326/control/hotairduct"
tempHotAirThreashold = 15

#temparature range that allowed
tempCanChange = 2




def on_message_for_cold_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    print(data)


client.message_callback_add(tempColdAirSensorTopic, on_message_for_temp)
client.connect("vpn.ce.pdn.ac.lk", port=8883)
client.subscribe("326/sensor/#")
client.loop_forever()
