import redis

r = redis.Redis(host='172.17.0.4', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('alerts')

print("Ожидание уведомлений...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Новое уведомление: {message['data']}")
