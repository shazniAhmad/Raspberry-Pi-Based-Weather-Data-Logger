import sys
import Adafruit_DHT
import time
import datetime

import logging
logging.basicConfig(level=logging.DEBUG)

import RPi.GPIO as GPIO

import paho.mqtt.client as mqtt

relay_state = "LOW"
channel = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(channel,GPIO.OUT)
GPIO.output(channel,False)

#setting up MQTT broker settings
BROKER_IP = "test.mosquitto.org"
BROKER_PORT = 1883
MQTT_TOPIC = "date_time_hum_temp"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT connection established")
    else:
        print("MQTT connection failed, return code %d/n", rc)

def send_data_to_broker(humidity,temperature,relay_state):
    payload = {
        "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity,
        "relay_state": relay_state
    }
    print("Data published to broker")
    client.publish(MQTT_TOPIC, str(payload))
    
#setting up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
    

try:
    client.connect(BROKER_IP,BROKER_PORT)
    client.loop_start()
    
    while True:
    
        humidity,temperature = Adafruit_DHT.read_retry(11,4)
             
        now = datetime.datetime.now()
        #print(now.strftime("%d-%m-%y %H:%M:%S"))
        #print (now.strftime("%Y-%m-%d %H:%M:%S"),'Temp: {0:0.1f} C,  Humidity: {1:0.1f}%, '.format(temperature,humidity),'Relay state is',relay_state)
        
        #send_data_to_broker(humidity,temperature,relay_state)
            
        
        
        
        GPIO.output(8,GPIO.LOW)
        
         
        if  60 > humidity > 50 :
            GPIO.output(8,GPIO.HIGH)
            GPIO.output(channel,GPIO.HIGH)
            relay_state = "HIGH"
            #print ("Relay state is",relay_state)
        else :
            GPIO.output(8,GPIO.LOW)
            GPIO.output(channel,GPIO.LOW)
            relay_state = "LOW"
            #print ("Relay state is",relay_state)
        
        print (now.strftime("%Y-%m-%d %H:%M:%S"),'Temp: {0:0.1f} C,  Humidity: {1:0.1f}%, '.format(temperature,humidity),'Relay state is',relay_state)
        send_data_to_broker(humidity,temperature,relay_state)
        
        time.sleep(1)
            
except KeyboardInterrupt:
    print("Exitting the command flow")
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()