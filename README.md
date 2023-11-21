# Raspberry-Pi-Based-Weather-Data-Logger
A Raspberry Pi 3b module is used to measure weather data using a DHT11  module, and a relay is operated based on the collected data. All these data are  displayed real time and are published to a MQTT topic of Mosquitto MQTT broker.  Then a python script is developed to subsribe to that topic and insert the data into  PostgreSQL database.
