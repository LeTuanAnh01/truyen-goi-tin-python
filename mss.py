import time
import threading
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883


pubtop = "/boxchat/tu"
subtop = "/boxchat/tuan"


client_id = f'python-mqtt-{10}' #connect to broker
username = 'emqx'
password = 'public'

# connect client to broker
def on_connect(client, userdata, flags, rc): #call to connect function
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(subtop)
        
    else:
        print("Failed to connect, return code %d\n", rc)

###########################

# message control

def on_message(client, userdata, msg):  
    global chat
    if str(msg.topic) != pubtop:  
        chat = str(msg.payload.decode("utf-8"))
        print("\nCustom :", chat)
       
def publish(client):
    global msg
    while True:
        msg = input("You :")
        if msg == 'stop' or msg == 'Stop':
            client.disconnect()
            print("Disconnected....")
            break
        else: 
            client.publish(pubtop,msg,0, retain=False)      
            
def on_disconnect(client, userdata, rc):

    if rc != 0:
        print("Unexpected disconnection.")
        client.disconnect()

client = mqtt_client.Client(client_id, clean_session = False,userdata=None)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker,port)

time.sleep(1)
thread1 =threading.Thread(target=publish,args=(client,))
thread1.start()

client.loop_forever()
 
    


 
    








