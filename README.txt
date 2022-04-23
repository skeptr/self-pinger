# Self-Pinger
## Проект для изучения основных принципов работы с docker


## Переменные окружения
### Переопределить название
export SELF_PINGER_NAME=MyAppName

### Вывод дополнительных сообщений
export SELF_PINGER_DEBUG=1

### Вернуть 403 на каждый n-ный GET-запрос
export SELF_PINGER_PERIOD=3


## Запуск с помощью docker run
### Сборка образа
docker image build -t self-pinger .

### Простой запуск контейнера
docker run -p 8000:8000 \
-e SELF_PINGER_NAME \
-e SELF_PINGER_DEBUG \
-e SELF_PINGER_PERIOD \
self-pinger


## Запуск через docker-compose
docker-compose build
docker-compose run self-pinger


## Проверка работоспособности
### Основная функция
curl http://localhost:8000/ping

### Сводная информация о службе, включая счётчик обработанных запросов
curl http://localhost:8000/
