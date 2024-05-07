from fastapi import FastAPI
from app.configs.broker_configs import mqtt_broker_configs
from fastapi_mqtt import FastMQTT, MQTTConfig
from .database import engine
from app import models, schemas
from app.routers import gate_router
from app.mqtt.database_mqtt import saveDataInDB
from datetime import datetime, timezone
import json

# cria todas as tabelas necessárias do db
models.Base.metadata.create_all(bind=engine)
connection = engine.connect()

mqtt_config = MQTTConfig(
    host=mqtt_broker_configs.get('HOST'), 
    port=mqtt_broker_configs.get('PORT'), 
    keepalive=mqtt_broker_configs.get('KEEPALIVE'),
    will_message_topic=mqtt_broker_configs.get('TOPIC'),
    will_message_payload="MQTT Connection is dead!",
    # will_delay_interval=2,
)

fast_mqtt = FastMQTT(
    config=mqtt_config
)

app = FastAPI()

app.include_router(gate_router.router)

fast_mqtt.init_app(app)


@fast_mqtt.on_connect()
def connect(client, flags: int, rc: int, properties):
    client.subscribe(mqtt_broker_configs.get('TOPIC'))  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic: str, payload, qos: int, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)

    # Usando json.loads() para converter a string JSON em um dicionário Python
    result = json.loads(payload.decode())

    print(f"Result: {result['id']}")

    mqtt_data = schemas.MQTTData(gate_id=result['id'], gate_state=result['estado'], time=datetime.now(timezone.utc))

    saveDataInDB(mqttData=mqtt_data)



@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid: int, qos: int, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/test")
async def func():
    return {"message": "Hello World"}
