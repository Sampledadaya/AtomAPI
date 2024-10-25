### Разработать API атом чата, в котором пользователи могут общаться друг с другом в приватных каналах.

1. Реализовать регистрацию новых пользователей и авторизацию.
2. Предусмотреть роль модератора, которому доступны все каналы и предоставлена возможность блокировки пользователей.
3. Сообщения должны отправляться в режиме "реального времени".
4. Пользователям доступен функционал просмотра истории сообщений.

## Установка и запуск

### 1. Клонирование репозитория

Сначала клонируйте репозиторий на свою локальную машину:

```
https://github.com/Sampledadaya/AtomAPI.git
cd chat_project
```
### 2. Запуск проекта
```
docker-compose up --build
```

P.s. Делал проект в PyCharm, рекомендую использовать его для запуска. После запуска можно перейти по ссылке в браузере - localhost:8000, где уже и можно будет увидеть API.
## Тестирование функционала

### 1. Авторизация 
```
curl -X POST http://localhost:8000/api/api/login/ \
-H "Content-Type: application/json" \
-d '{"username": "new_user", "password": "new_password"}'
```

### 2. Создание канала
```
curl -X POST http://localhost:8000/api/api/channels/ \
-H "Content-Type: application/json" \
-H "X-CSRFToken: $(grep csrftoken cookies.txt | cut -f 7)" \
-b cookies.txt \
-d '{"name": "New Channel", "description": "Description of the new channel"}'
```

### 3. Получение списка каналов
```
curl -X GET http://localhost:8000/api/api/channels/ \
-b cookies.txt
```

### 4. Отправка сообщений в канал
```
curl -X POST http://localhost:8000/api/api/channels/1/send_message/ \
-H "Content-Type: application/json" \
-H "X-CSRFToken: $(grep csrftoken cookies.txt | cut -f 7)" \
-b cookies.txt \
-d '{"content": "Привет всем!"}'
```

### 5. История сообщений из канала 
```
curl -X GET http://localhost:8000/api/api/channels/1/messages/ \
-b cookies.txt
```
### 6. Блокировка пользователя
```
curl -X POST http://localhost:8000/api/api/users/3/block/ \
-H "Content-Type: application/json" \
-H "X-CSRFToken: $(grep csrftoken cookies.txt | cut -f 7)" \
-b cookies.txt
```
P.S. - Учетная запись с уже готовыми правами - username: "admin" password: "admin"
### P.S. 
#### Для того, чтобы блокировать пользователей и видеть весь список каналов 
#### необходимо зайти под аккаунтом, который находится в группе модератор, внести в нее 
#### мы можем через админку в разделе группы (группа- Модератор)
#### Так же мы можем добавлять через запросы в канал пользователей, чтобы они тоже 
#### могли в них отправлять сообщения. Все тестирования делались через терминал, так
#### же можно протестировать через Postman
#### Проект с реализацией отправки сообщений в реальном времени делал в первый  раз
#### Джанго сейчас активно изучаю, но начал совсем недавно, и очень надеюсь, что
#### в вашей команде смогу улучшить свои навыки на практике, решая интересные и 
#### нестандартные задачи.
