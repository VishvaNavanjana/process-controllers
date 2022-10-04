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
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return
    
    temperature = values[1]
    print("Received Temperature " + str(temperature))
    
    if (temperature > (tempColdAirThreashold + tempCanChange)):
        client.publish(tempColdAirControlTopic , "Chiller ON")
        print("published 'Chiller ON' to topic " + tempColdAirControlTopic)
    #on desired temparatures
    elif (temperature < (tempColdAirThreashold + tempCanChange) and  temperature > (tempColdAirThreashold - tempCanChange)):
        client.publish(tempColdAirControlTopic , "Chiller OFF")
        print("published 'Chiller OFF' to topic " + tempColdAirControlTopic)

    print()
    

def on_message_for_hot_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return
    
    temperature = values[1]
    print("Received Temperature " + str(temperature))
    
    if (temperature < (tempHotAirThreashold - tempCanChange)):
        client.publish(tempHotAirControlTopic , "Boiler ON")
        print("published 'Boiler ON' to topic " + tempHotAirControlTopic)
    #on desired temparatures
    elif (temperature < (tempHotAirThreashold + tempCanChange) and  temperature > (tempColdAirThreashold - tempCanChange)):
        client.publish(tempHotAirControlTopic , "Boiler OFF")
        print("published 'Boiler OFF' to topic " + tempHotAirControlTopic)

    print()




client.message_callback_add(tempColdAirSensorTopic, on_message_for_cold_air_duct)
client.message_callback_add(tempHotAirSensorTopic, on_message_for_hot_air_duct)
client.connect(mqttBroker, port=8883)
client.subscribe("326/sensor/#")
client.loop_forever()
