import paho.mqtt.client as mqtt
import json

mqttBroker = "vpn.ce.pdn.ac.lk"
client = mqtt.Client("boiler-chiller-controller")

#Air flowrate mqtt topic
airFlowrateSensorTopic = "326/sensor/coldairduct"  #subscriber
airFlowrateControlTopic = "326/control/coldairduct"     #publisher
airFlowrateThreashold = 25

#flowrate allowed
flowrateCanChange = 2

def on_message_for_airflow(client, userdata, message):

    data = json.loads(message.payload)
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())

    #check 'airflow'
    if (length != 2 or keys[0] != 'time' or keys[1] != 'airflow'):
        return
    
    airFlowrate = values[1]
    print("Received Air Flowrate from cold air duct " + str(airFlowrate))
    
    if (airFlowrate > (airFlowrateThreashold + flowrateCanChange)):
        client.publish(airFlowrateControlTopic , "Provide Outside Air")
        print("published 'Provide Outside Air' to topic " + airFlowrateControlTopic)

    #on desired tairFlowRates
    elif (airFlowrate < (airFlowrateThreashold - flowrateCanChange) ):
        client.publish(airFlowrateControlTopic , "Remove inside air")
        print("published 'Remove inside air' to topic " + airFlowrateControlTopic)

    # ==
    else:
        client.publish(airFlowrateControlTopic , "Maintain current flowrate")
        print("published 'Maintain current flowrate' to topic " + airFlowrateControlTopic)


    print()

client.message_callback_add(airFlowrateSensorTopic, on_message_for_airflow)
client.connect(mqttBroker, port=8883)
client.subscribe("326/sensor/coldairduct")
client.loop_forever()
