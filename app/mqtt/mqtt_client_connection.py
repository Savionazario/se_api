import paho.mqtt.client as mqtt
from app.configs.broker_configs import mqtt_broker_configs
from app.mqtt.callbacks import on_connect, on_subscribe, on_message

from fastapi_mqtt import FastMQTT, MQTTConfig


# def startConnection():
#     mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, mqtt_broker_configs.get('CLIENT_NAME'))

#     # Setando as callbacks
#     mqtt_client.on_connect = on_connect
#     mqtt_client.on_subscribe = on_subscribe
#     mqtt_client.on_message = on_message

#     # Conectando com o broker
#     mqtt_client.connect(host=mqtt_broker_configs.get('HOST'), port=mqtt_broker_configs.get('PORT'), keepalive=mqtt_broker_configs.get('KEEPALIVE'))

#     mqtt_client.loop_forever()


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
