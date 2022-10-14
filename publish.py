import os
import time
import paho.mqtt.client as mqtt
import json
import socket
from dotenv import load_dotenv

from lghub import LGHUB


load_dotenv()

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
# DEVICE = "logitech_g703_new"
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

def mqtt_on_disconnect(client, userdata, rc=0):
    print("Disconnected result code "+str(rc))
    client.loop_stop()

def mqtt_on_log(client, userdata, level, buf):
    print("log: ", buf)

def mqtt_on_publish(client, userdata, mid):
    print("published:", client, userdata, mid)

def publish_to_mqtt():
    client = mqtt.Client(DEVICE)
    client.will_set(LWT_TOPIC, payload="Offline", qos=0, retain=True)
    client.on_connect = mqtt_on_connect
    client.on_disconnect = mqtt_on_disconnect
    client.on_publish = mqtt_on_publish
    client.on_log = mqtt_on_log
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    client.connect(MQTT_BROKER, keepalive=60)
    client.loop_start()
    # client.loop_forever(retry_first_connection=True)
    try:
        while True:
            info = LGHUB().data_to_publish()
            client.publish(f"{TOPIC}/error", info["error"], retain=True)
            client.publish(f"{TOPIC}/timestamp", info["timestamp"], retain=True)
            client.publish(f"{TOPIC}/last_update", info["last_update"], retain=True)
            client.publish(f"{TOPIC}/last_refresh", info["last_refresh"], retain=True)
            client.publish(f"{TOPIC}/level", info["level"], retain=True)
            client.publish(f"{TOPIC}/is_charging", info["is_charging"], retain=True)
            client.publish(f"{TOPIC}/hours_remaining", info["hours_remaining"], retain=True)
            client.publish(f"{TOPIC}/STATE", json.dumps(info), retain=True)
            print(f"Published.. {info}")
            time.sleep(30)
    except KeyboardInterrupt:
        client.loop_stop()
    except socket.error:
        print("[ERROR] Reconnecting..")
        client.loop_stop()
        publish_to_mqtt()

# failed to receive on socket: [WinError 10054] An existing connection was forcibly closed by the remote host
