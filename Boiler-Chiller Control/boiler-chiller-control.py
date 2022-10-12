import paho.mqtt.client as mqtt
import json
import datetime

mqttBroker = "vpn.ce.pdn.ac.lk"
client = mqtt.Client("boiler-chiller-controller")

#temperature at cold air duct
tempColdAirSensorTopic = "326project/smartbuilding/hvac/coldairduct/temperature" 
tempColdAirControlTopic = "326project/smartbuilding/hvac/control/chiller"
tempColdAirScadaTopic =  "326project/smartbuilding/hvac/scada/state/chiller"
tempColdAirThreashold = 25 #default

#temparature at hot air duct
tempHotAirSensorTopic = "326project/smartbuilding/hvac/hotairduct/temperature"
tempHotAirControlTopic = "326project/smartbuilding/hvac/control/boiler"
tempHotAirScadaTopic = "326project/smartbuilding/hvac/scada/state/boiler"
tempHotAirThreashold = 15 #default

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
    print("Received Temperature from cold air duct " + str(temperature))
    
    if (temperature > (tempColdAirThreashold + tempCanChange)):
        # Chiller On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
        }
        
        #publish to scada
        client.publish(tempColdAirScadaTopic,json.dumps(x))
        #publish to controller
        client.publish(tempColdAirControlTopic, json.dumps(x))
        print("published 'Chiller ON' to topic " + tempColdAirControlTopic)
        
    #on desired temparatures
    elif (temperature < (tempColdAirThreashold + tempCanChange) and  temperature > (tempColdAirThreashold - tempCanChange)):
        # Chiller Off
         x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
         client.publish(tempColdAirScadaTopic,json.dumps(x))
         client.publish(tempColdAirControlTopic, json.dumps(x))
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
    print("Received Temperature from hot air duct " + str(temperature))
    
    if (temperature < (tempHotAirThreashold - tempCanChange)):
        # Boiler On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
            }
        client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(tempHotAirControlTopic , json.dumps(x))
        print("published 'Boiler ON' to topic " + tempHotAirControlTopic)
        
    #on desired temparatures
    elif ((temperature < (tempHotAirThreashold + tempCanChange)) and  (temperature > (tempColdAirThreashold - tempCanChange))):
        
        print("Hot air duct temperature in range")
        
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
        client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(tempHotAirControlTopic , json.dumps(x))
        print("published 'Boiler OFF' to topic " + tempHotAirControlTopic)

    print()




print("Boiler-Chiller-Controller Started.............")
client.message_callback_add(tempColdAirSensorTopic, on_message_for_cold_air_duct)
client.message_callback_add(tempHotAirSensorTopic, on_message_for_hot_air_duct)
client.connect(mqttBroker, port=8883)
client.subscribe("326project/smartbuilding/hvac/#")
client.loop_forever()
