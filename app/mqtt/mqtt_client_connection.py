import paho.mqtt.client as mqtt
from app.configs.broker_configs import mqtt_broker_configs
from fastapi_mqtt import FastMQTT, MQTTConfig

def startConnection():
    mqtt_config = MQTTConfig(
        host=mqtt_broker_configs.get('HOST'), 
        port=mqtt_broker_configs.get('PORT'), 
        keepalive=mqtt_broker_configs.get('KEEPALIVE'),
    )

    fast_mqtt = FastMQTT(
        config=mqtt_config
    )

    return fast_mqtt
