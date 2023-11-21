import paho.mqtt.client as mqtt
import psycopg2
import json

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mqttvalues",
    user="postgres",
    password="123"
)

def on_connect(client, userdata, flags, rc):
    client.subscribe("payload")
    print(f"Connected")

def on_message(client, userdata, msg):
    # Callback function for MQTT message received
    if msg.topic == "payload":
        payload = json.loads(msg.payload)
        print(f'Payload inserted into database', payload)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute("INSERT INTO sensor_data (temperature, humidity, date_time) VALUES (%s, %s, %s)",
        (payload["temperature"], payload["humidity"], payload["date_time"]))

        # Commit the changes & close the cursor and database connection
        conn.commit()
        cursor.close()

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connection result:", client.connect(MQTT_BROKER, MQTT_PORT, 60))

client.loop_start()

while True:
    pass