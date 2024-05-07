from app.configs.broker_configs import mqtt_broker_configs

# Callback executada quando o client é conectado
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Cliente conectado com sucesso: {client}")
        client.subscribe(mqtt_broker_configs.get('TOPIC'))
    else:
        print(f"Erro ao me conectar! codigo = {rc}")

# Callback executada quando o client é subscrito em algum tópico
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Cliente subscribed at: {mqtt_broker_configs.get('TOPIC')}")
    print(f"QOS: {granted_qos}")

# Callback executada quando o client recebe alguma mensagem
def on_message(client, userdata, message):
    print(f"Mensagem recebida!")
    print(client)
    print(message.payload)