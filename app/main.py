from fastapi import FastAPI, Response, HTTPException, Depends
from app.configs.broker_configs import mqtt_broker_configs
from fastapi_mqtt import FastMQTT, MQTTConfig
from .database import engine
from app import models, schemas, database
from app.routers import gate_router
from app.mqtt.database_mqtt import saveDataInDB, saveConfigDataInDB
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session

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

get_db = database.get_db

@fast_mqtt.on_connect()
def connect(client, flags: int, rc: int, properties):
    client.subscribe("CondominioSensores")  # subscribing mqtt topic # subscribing mqtt topic
    client.subscribe("CondominioConfigs")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic: str, payload, qos: int, properties):
    # print("Received message: ", topic, payload.decode())

    if(topic == "CondominioSensores"):
        result = json.loads(payload.decode())
        
        for res in result:
            timenow = datetime.now(timezone.utc)
            current_state = False
            if res['estado'] == "ABERTO":
                current_state = True

            mqtt_data = schemas.MQTTData(gate_id=res['id'], gate_state=current_state, time=timenow)
            saveDataInDB(mqttData=mqtt_data)
    if(topic == "CondominioConfigs"):
        result = json.loads(payload.decode())

        alarme_estado = False
        alarme_enable_estado = False
        luz_externa = False

        if result["AlarmeEstado"] == "1":
            alarme_estado = True
        if result["AlarmeEnableEstado"] == "1":
            alarme_enable_estado = True
        if result["LuzExterna"] == "1":
            luz_externa = True

        condominioData = schemas.CondominiumData(alarme_estado=alarme_estado, alarme_enable_estado=alarme_enable_estado, luz_externa=luz_externa, tempo_esquecimento=result["TempoEsquecimentoEstado"], time=datetime.now(timezone.utc))

        saveConfigDataInDB(data=condominioData)



    


async def func():
    fast_mqtt.publish("/mqtt", "Hello from Fastapi")  # publishing mqtt topic
    return {"result": True, "message": "Published"}


@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid: int, qos: int, properties):
    print("subscribed", client, mid, qos, properties)

@app.post("/luzexterna/{luz_estado}", tags=["Luz externa"])
async def luz_externa(luz_estado: int):
    if luz_estado == 0 or luz_estado == 1:
        fast_mqtt.publish("LuzExternaConfig", f"{luz_estado}")  # publishing mqtt topic
        return {"result": True, "message": "Published"}
    raise HTTPException(status_code=500, detail="Estado incorreto!")

@app.post("/condominioConfigs", tags=["Configs"])
async def config(configs: schemas.CondominiumConfigs, db: Session = Depends(get_db)):
    try:
        alarme_enable = "0" if configs.alarme_enable_estado == False else "1"
        fast_mqtt.publish("AlarmeEnableConfig", alarme_enable)
        fast_mqtt.publish("TempoEsquecimentoConfig", f"{configs.tempo_esquecimento}")

        return {"message": "Configurações atualizadas com sucesso!"}
    except:
        raise HTTPException(status_code=500, detail="Algo deu errado!")

@app.get("/condominioConfigs", tags=["Configs"])
async def config(db: Session = Depends(get_db)):
    configs = db.query(models.CondominiumConfigs).first()

    return configs


