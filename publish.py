import os
import time
import paho.mqtt.client as mqtt
import json
from xml_file import battery_info
from dotenv import load_dotenv

load_dotenv()

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
FILENAME = "g_hub_settings.json"
FILE_PATH = DIR_PATH + FILENAME
DEVICE = "logitech_g703"
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
LWT_TOPIC = f"tele/{DEVICE}/LWT"
TOPIC = f"stat/{DEVICE}"

def mqtt_on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to broker.")
        client.publish(LWT_TOPIC, payload="Online", qos=0, retain=True)
    else:
        raise ConnectionError("Failed to connect to broker.")

def publish_to_mqtt():
    client = mqtt.Client(DEVICE)
    client.will_set(LWT_TOPIC, payload="Offline", qos=0, retain=True)
    client.on_connect = mqtt_on_connect
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    client.connect(MQTT_BROKER, keepalive=300)
    while True:
        info = battery_info()
        client.loop_start()
        client.publish(f"{TOPIC}/error", info["error"], retain=True)
        client.publish(f"{TOPIC}/timestamp", info["timestamp"], retain=True)
        client.publish(f"{TOPIC}/last_update", info["last_update"], retain=True)
        client.publish(f"{TOPIC}/name", info["name"], retain=True)
        client.publish(f"{TOPIC}/level", info["level"], retain=True)
        client.publish(f"{TOPIC}/is_charging", info["is_charging"], retain=True)
        client.publish(f"{TOPIC}/STATE", json.dumps(info), retain=True)
        print(f"Published.. {info}")
        time.sleep(60)
        client.loop_stop()


