import redis
import time

r = redis.Redis(host='172.17.0.4', port=6379, decode_responses=True)

while True:
    msg = input("Введите уведомление (или 'exit' для выхода): ")
    if msg.lower() == "exit":
        break
    r.publish('alerts', msg)
    print("Уведомление отправлено!")
