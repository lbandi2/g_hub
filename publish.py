import os
import time
import paho.mqtt.client as mqtt
import json
import socket
import logging
from dotenv import load_dotenv

from lghub import LGHUB

logger = logging.getLogger()

load_dotenv()

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
DEVICE = "logitech_g703"
LWT_TOPIC = f"tele/{DEVICE}/LWT"
TOPIC = f"stat/{DEVICE}"

def mqtt_on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.publish(LWT_TOPIC, payload="Online", qos=0, retain=True)
        logger.info("Connected to MQTT broker")
    else:
        logger.error("Failed to connect to MQTT broker")
        # raise ConnectionError("Failed to connect to broker")

# def mqtt_on_disconnect(client, userdata, rc=0):
def mqtt_on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT broker, trying to reconnect", str(rc))
    # print("Disconnected result code "+str(rc))
    # client.loop_stop()
    if rc != 0:
        logger.warning("Disconnected from MQTT broker, trying to reconnect", str(rc))
        # print(f"Unexpected MQTT disconnection with code {str(rc)}. Will auto-reconnect")

def publish_to_mqtt(broker, user, password):
    # LWT = f"tele/{device_name}/LWT"
    # TOPIC = f"stat/{device_name}"
    client = mqtt.Client(DEVICE)
    client.username_pw_set(username=user, password=password)
    client.will_set(LWT_TOPIC, payload="Offline", qos=0, retain=True)
    client.on_connect = mqtt_on_connect
    client.on_disconnect = mqtt_on_disconnect

    while not client.is_connected():
        client.connect_async(broker, keepalive=60)
        client.loop_start()
        logger.info(f"Trying to connect to broker at {broker}")
        time.sleep(15)

    try:
        while True:
            try:
                info = LGHUB().data_to_publish()
                if info["is_charging"]:
                    logger.info("Device is charging")
            except Exception as e:
                logger.critical("Program crashed with error", exc_info=True)
            finally:
                client.is_connected()
                client.publish(f"{TOPIC}/level", info["level"], retain=True)
                client.publish(f"{TOPIC}/is_charging", info["is_charging"], retain=True)
                client.publish(f"{TOPIC}/hours_remaining", info["hours_remaining"], retain=True)
                client.publish(f"{TOPIC}/error", info["error"], retain=True)
                client.publish(f"{TOPIC}/timestamp", info["timestamp"], retain=True)
                client.publish(f"{TOPIC}/last_update", info["last_update"], retain=True)
                client.publish(f"{TOPIC}/last_refresh", info["last_refresh"], retain=True)
                client.publish(f"{TOPIC}/STATE", json.dumps(info), retain=True)
                logger.debug(f"Published {info}")
                time.sleep(30)
    except KeyboardInterrupt:
        logger.warning("Aborted from keyboard")
        client.loop_stop()
        logger.info("Exiting main program")
    except socket.error:
        logger.warning("Connection interrupted by Windows, reconnecting")
        client.loop_stop()
        logger.info("Exiting main program")
        publish_to_mqtt()
    except Exception as e:
        logger.critical("Program crashed with error", exc_info=True)

# failed to receive on socket: [WinError 10054] An existing connection was forcibly closed by the remote host
