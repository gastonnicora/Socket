
import redis
from os import environ
import threading
import json

redis_host = environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379)


 
# Función para manejar mensajes de Redis
def handle_message(message):
    if message['type'] == 'message':
        data = json.loads(message['data'])
        task_name = data['task_name']
        if task_name in tasks:
            tasks[task_name](data)

# Suscripción a mensajes de Redis
def subscribe_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(**{'task_socket_channel': handle_message})
    print('Listening for messages on task_channel...')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_message(message)

# Iniciar la suscripción a Redis en un hilo separado
def run_redis_subscriber():
    thread = threading.Thread(target=subscribe_to_redis)
    thread.start()


def emit_bid(data):
    from app.socketio import emit_bid
    emit_bid(data["data"])
    return

def emit_finish(data):
    from app.socketio import emit_finish
    emit_finish(data["room"])
    return

def emit_start(data):
    from app.socketio import emit_start
    emit_start(data["room"],data["time"])
    return

def start(data):
    from app.socketio import start
    start(data["room"])
    return

def emit_updateSesion(data):
    from app.socketio import emit_updateSesion
    emit_updateSesion(data["data"])
    return

tasks = {
    "emit_bid": emit_bid,
    "emit_finish": emit_finish,
    "emit_start": emit_start,
    "start":start,
    "emit_updateSesion":emit_updateSesion

}
