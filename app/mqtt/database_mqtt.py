from fastapi import APIRouter, Depends, Path, Response, status
from app import schemas, models, database
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


def saveDataInDB(mqttData: schemas.MQTTData):
    with contextmanager(get_db)() as db:
        gate = db.query(models.Gate).filter(models.Gate.gate_id == mqttData.gate_id).first()
        if not gate:
            new_gate = models.Gate(gate_id=mqttData.gate_id, current_state=mqttData.gate_state, time=mqttData.time)
            db.add(new_gate)
            db.commit()
            db.refresh(new_gate)

            print("Portão novo Cadastrado!")
            
        else:
            gate.time = mqttData.time
            db.commit()
            db.refresh(gate)

            # Recuperando o ultimo status do gate
            gate_last_status = db.query(models.GateStateHistory).filter(models.GateStateHistory.gate_id == gate.gate_id).order_by(desc(models.GateStateHistory.time)).first()

            if not gate_last_status:
                print("Gate not have historic")
                
                gate.current_state = mqttData.gate_state
                new_gate_data = models.GateStateHistory(gate_id=mqttData.gate_id, gate_state=mqttData.gate_state, time=mqttData.time)
                db.add(new_gate_data)
                db.commit()
                db.refresh(new_gate_data)
                db.refresh(gate)

            else:
                if (gate_last_status.gate_state != mqttData.gate_state): # Verificando se o valor recebido é igual ao ultimo salvo no db
                    gate.current_state = mqttData.gate_state
                    new_gate_data = models.GateStateHistory(gate_id=mqttData.gate_id, gate_state=mqttData.gate_state, time=mqttData.time)
                    db.add(new_gate_data)
                    db.commit()
                    db.refresh(new_gate_data)
                    db.refresh(gate)
                else:
                    print("Nada mudou!")

def saveConfigDataInDB(data: schemas.CondominiumData):
    with contextmanager(get_db)() as db:
        config = db.query(models.CondominiumConfigs).first()

        if not config:
            new_config = models.CondominiumConfigs(alarme_estado= data.alarme_estado, alarme_enable_estado=data.alarme_enable_estado, luz_externa=data.luz_externa, tempo_esquecimento=data.tempo_esquecimento, time=data.time)
            db.add(new_config)
            db.commit()
            db.refresh(new_config)
        else:
            config.alarme_estado = data.alarme_estado
            config.alarme_enable_estado = data.alarme_enable_estado
            config.luz_externa = data.luz_externa
            config.tempo_esquecimento = data.tempo_esquecimento
            config.time = data.time

            db.commit()
            db.refresh(config)

def saveRFID(codigo, time):
    with contextmanager(get_db)() as db:
        rfid = models.RFID(codigo=codigo, time=time)
        db.add(rfid)
        db.commit()
        db.refresh(rfid)
