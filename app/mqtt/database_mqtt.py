from fastapi import APIRouter, Depends, Path, Response, status
from app import schemas, models, database
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db


def saveDataInDB(mqttData: schemas.MQTTData):
    db = next(get_db())

    gate = db.query(models.Gate).filter(models.Gate.gate_id == mqttData.gate_id).first()
    if not gate:
        print("Portão não encontrado!")
        
    else:
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
            print(f"Gate id: {gate_last_status.gate_id}")
            print(f"Gate state: {gate_last_status.gate_state}")
            print(f"Gate time: {gate_last_status.time}")

            if (gate_last_status.gate_state != mqttData.gate_state): # Verificando se o valor recebido é igual ao ultimo salvo no db
                gate.current_state = mqttData.gate_state
                new_gate_data = models.GateStateHistory(gate_id=mqttData.gate_id, gate_state=mqttData.gate_state, time=mqttData.time)
                db.add(new_gate_data)
                db.commit()
                db.refresh(new_gate_data)
                db.refresh(gate)
            else:
                print("Nothing is changed!")