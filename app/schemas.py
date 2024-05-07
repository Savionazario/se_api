from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MQTTData(BaseModel):
    gate_id: str
    gate_state: bool
    time: datetime

    class Config:
        orm_mode = True

class Gate(BaseModel):
    name: str
    # current_state: bool

    class Config:
        orm_mode = True

class GateStatus(BaseModel):
    gate_state: bool
    time: datetime

    class Config:
        orm_mode = True

class CondominiumData(BaseModel):
    alarme_enable_estado: bool
    alarme_estado: bool
    tempo_esquecimento: int
    luz_externa: bool
    time: datetime

    class Config:
        orm_mode = True

class CondominiumConfigs(BaseModel):
    alarme_enable_estado: bool
    tempo_esquecimento: int

    class Config:
        orm_mode = True


