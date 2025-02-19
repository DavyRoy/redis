# Redis

---

### Задание 1 - Введение в Redis

1. `Настройка Redis в Docker`
2. `Выполни следующие команды: Сохрани в Redis ключ mykey со значением "Hello, World!". Получи значение ключа mykey. Удали ключ mykey. Установи TTL для нового ключа на 30 секунд. Сохрани несколько данных в хэш и извлеки их.`

``` ~Решение~
1.
docker run --name redis -d redis
docker exec -it redis redis-cli
2.
SET mykey "Hello, Redis!"
GET mykey
DEL mykey
EXPIRE mykey 60
HSET user:1 name "John" age 30
HGET user:1 name
HGET user:1 age
....
```

`Cкриншоты
![Cкриншот 1](ссылка на скриншот 1)`

---

### Задание 2 - Структуры данных Redis

1. `Строки: Создай строковый ключ с именем "counter" и установи его значение равным 10. Увеличь это значение на 5 с помощью команды INCR. Установи срок годности этого ключа на 30 секунд с помощью команды EXPIRE.`
2. `Хэши: Создай хэш для пользователя с ключом user:123, где поля будут: name, age, email. Добавь в хэш соответствующие значения. Извлеки все поля из хэша с помощью HGETALL.`
3. `Списки: Создай список с задачами: "Task 1", "Task 2", "Task 3". Извлеки задачи с помощью команды LRANGE и покажи все элементы списка. Удали одну задачу с помощью команды LPOP.`
4. `Множества: Создай множество с элементами "apple", "banana", "cherry". Извлеки все элементы множества с помощью SMEMBERS.`
5. `Упорядоченные множества: Создай упорядоченное множество с элементами: "Alice" (балл 200), "Bob" (балл 150), "John" (балл 100). Покажи все элементы с баллами с помощью команды ZRANGE.`

``` ~Решение~
1.
SET counter 10
INCRBY counter 5
EXPIRE counter 30
2.
IHSET user:123 name "Tom" age "30" email "tom@example.com"
HGETALL user:123
3.
LPUSH task "Task 1"
LPUSH task "Task 2"
LPUSH task "Task 3"
LRANGE task 0 -1
  1) "Task 3"
  2) "Task 2"
  3) "Task 1"
LPOP task 1
LRANGE task 0 -1
  1) "Task 2"
  2) "Task 1"
4.
SADD fruits "apple" "banana" "cherry"
SMEMBERS fruits
  1) "apple"
  2) "banana"
  3) "cherry"
5.
ZADD leaderboard 200 "Alice" 150 "Bob" 100 "John"
ZRANGE leaderboard 0 -1 WITHSCORES
  1) "John"
  2) "100"
  3) "Bob"
  4) "150"
  5) "Alice"
  6) "200"
....
```

`Cкриншоты
![docker-node.png](https://github.com/DavyRoy/docker/blob/main/my-node/images/docker-node.png)`

---

### Задание 3 - Продвинутые возможности Redis

1. `Cоздайте транзакцию, которая: Добавляет новый ключ counter со значением 0. Инкрементирует его три раза. Устанавливает время жизни на 60 секунд.`
2. `Pub/Sub: Запустите подписку на канал notifications. Опубликуйте в него несколько сообщений. Проверьте, как они доходят до подписчиков.`
3. `Реализация системы уведомлений в реальном времени`

``` ~Решение~
1.
MULTI
SET counter 0
EXPIRE counter 30
INCR counter
INCR counter
INCR counter
EXEC
2.
SUBSCRIBE notifications
  PUBLISH notifications "Hello!"
1) "message"
2) "notifications"
3) "Hello!"
  PUBLISH notifications "News!"
1) "message"
2) "notifications"
3) "News!"
3.
pip install redis
nano subscriber.py
....
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('alerts')

print("Ожидание уведомлений...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Новое уведомление: {message['data']}")
....
nano publisher.py
....
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

while True:
    msg = input("Введите уведомление (или 'exit' для выхода): ")
    if msg.lower() == "exit":
        break
    r.publish('alerts', msg)
    print("Уведомление отправлено!")
....
python subscriber.py
python publisher.py
....
```

`Cкриншоты
![Pub](https://github.com/DavyRoy/docker/blob/main/docker-network/images/docker-network.png)`

---

### Задание 4 - Репликация и кластеризация Redis

1. `Настроить репликацию Redis: Запустить мастер и слейв в Docker. Создать ключ в мастере, убедиться, что он есть в слейве.`
2. `Настроить Redis Cluster: Запустить кластер из 6 нод. Проверить распределение данных между нодами.`

``` ~Решение~
1.
docker network create redis-net
docker run -d --name redis-master --network redis-net \
  -p 6379:6379 redis:latest
docker run -d --name redis-slave --network redis-net \
  -p 6380:6379 redis:latest redis-server --replicaof redis-master 6379
docker exec -it redis-master redis-cli
  SET key1 "Hello from master"
docker exec -it redis-slave redis-cli
  GET key1
2.
docker network create redis-cluster-net
for i in {1..6}; do 
  docker run -d --name redis-node-$i --network redis-cluster-net \
  redis:latest redis-server --cluster-enabled yes --appendonly yes;
done
docker network inspect redis-cluster-net | grep IPv4
  "IPv4Address": "172.24.0.5/16",
  "IPv4Address": "172.24.0.2/16",
  "IPv4Address": "172.24.0.6/16",
  "IPv4Address": "172.24.0.7/16",
  "IPv4Address": "172.24.0.3/16",
  "IPv4Address": "172.24.0.4/16",
docker exec -it redis-node-1 redis-cli --cluster create \
  172.24.0.5:6379 172.24.0.2:6379 172.24.0.6:6379 172.24.0.7:6379 172.24.0.3:6379 172.24.0.4:6379 \
  --cluster-replicas 1
....
```

`Скриншоты
![Скриншот ](ссылка на скриншот)`

---
