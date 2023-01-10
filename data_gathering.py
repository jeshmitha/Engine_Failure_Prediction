import csv
import time
import paho.mqtt.client as paho
broker="192.168.4.1"
port=1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Data/modules")

def on_publish(client,userdata,result):
    print("data published \n")
    pass

def on_message(client, userdata, msg):
    print("Recieved Data:"+msg.payload.decode()+":")
    data = msg.payload.decode()
    listt = data[1:].split(" ")
    with open("Train4.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(listt)
        csvfile.close()
        print(listt)


client1= paho.Client("control1")
client1.on_publish = on_publish
client1.on_connect = on_connect
client1.on_message = on_message
client1.connect(broker,port)


client1.loop_forever()
