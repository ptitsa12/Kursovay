# Procurement System — REST API закупок

Django 4.2 + DRF + PostgreSQL 15 + JWT + Docker.

## Быстрый старт

```bash
docker compose up --build
```

После запуска:

| Сервис | URL |
|--------|-----|
| API | http://localhost:8000/api/ |
| Swagger | http://localhost:8000/api/docs/ |
| Админка | http://localhost:8000/admin/ |

## Тестовые пользователи

| Логин | Пароль | Роль |
|-------|--------|------|
| admin | admin123 | Суперпользователь |
| storekeeper | testpass123 | Кладовщик |
| purchaser | testpass123 | Закупщик |
| accountant | testpass123 | Бухгалтер |
| manager | testpass123 | Руководитель |

## JWT

```http
POST http://localhost:8000/api/token/
Content-Type: application/json

{"username": "storekeeper", "password": "testpass123"}
```

Заголовок для запросов: `Authorization: Bearer <access_token>`

## Postman

Импортируйте `postman/Procurement_API.postman_collection.json` и окружение `postman/Local.postman_environment.json`.  
После запроса **Get Token** переменная `token` обновится автоматически.

## Формат ошибок

```json
{"error": true, "message": "Текст ошибки"}
```

При ошибке поставщика (422):

```json
{"error": true, "message": "...", "alternatives": [...]}
```

## Подготовка к защите

1. `docker compose up --build` — проверить до защиты.
2. Открыть: терминал (логи), Postman, админку, IDE.
3. Сохранить токены всех 4 ролей в Postman.
4. Прогнать сценарий из чек-листа в отчёте.

## Проверка API в Postman

### Подготовка

1. Запустите API: `docker compose up --build`
2. Убедитесь, что сервис отвечает: http://localhost:8000/api/

### Импорт коллекции и окружения

1. Откройте Postman (десктоп или https://web.postman.co).
2. **Импорт коллекции** (все HTTP-запросы API):
   - **Import** → вкладка **File** (или перетащите файл)
   - выберите `postman/Procurement_API.postman_collection.json`
   - подтвердите импорт — появится коллекция **Procurement API** с папками: Auth, Requests, Orders, Finance, Warehouse.
3. **Импорт окружения** (переменные `base_url` и `token`):
   - снова **Import**
   - выберите `postman/Local.postman_environment.json`
   - появится окружение **Procurement Local**.
4. В правом верхнем углу Postman выберите окружение **Procurement Local** (должно быть активно, не «No environment»).

В окружении задано:
- `base_url` = `http://localhost:8000`
- `token` — заполняется автоматически после запросов на получение JWT

### Авторизация

Коллекция настроена на Bearer-токен: `Authorization: Bearer {{token}}`.

1. В папке **Auth** выполните нужный запрос **Get Token (...)** (storekeeper, purchaser, manager).
2. В **Tests** запроса скрипт сохраняет `access` в переменную `token` — повторно вставлять токен вручную не нужно.
3. Для сценария с другой ролью снова вызовите соответствующий **Get Token** — `token` обновится.

Тестовые учётные записи — в таблице «Тестовые пользователи» выше.

### Рекомендуемый порядок проверок

| Шаг | Запрос | Роль (токен) | Ожидание |
|-----|--------|--------------|----------|
| 1 | Auth → **Unauthorized - Products without token** | без токена | 401 |
| 2 | Auth → **Get Token (storekeeper)** | — | 200, `token` установлен |
| 3 | Requests → **Create Request** | storekeeper | 201 |
| 4 | Requests → **List Requests** | storekeeper | 200 |
| 5 | Auth → **Get Token (purchaser)** | — | смена роли |
| 6 | Requests → **Accept Request** | purchaser | 200 |
| 7 | Orders → **Create Order - bad supplier** | purchaser | 422 + `alternatives` |
| 8 | Orders → **Create Order - good supplier** | purchaser | 201 |
| 9 | Auth → **Get Token (storekeeper)** | — | проверка прав |
| 10 | Orders → **Create Order - forbidden for storekeeper** | storekeeper | 403 |
| 11 | Finance → **Create Accountable Request** | purchaser | по ролям в API |
| 12 | Auth → **Get Token (manager)** | — | |
| 13 | Finance → **Approve Accountable Request** | manager | 200 |
| 14 | Warehouse → цепочка (Invoice → Acceptance → checks → Deviation) | storekeeper / accountant | по сценарию |

При ошибках в теле ответа: `{"error": true, "message": "..."}` (для 422 у заказа — ещё поле `alternatives`).

### Альтернатива: Swagger

Интерактивная документация: http://localhost:8000/api/docs/ — удобно для разового вызова, для защиты удобнее готовая коллекция Postman с предзаполненными телами и тестами на `token`.

### Перед защитой

1. Прогнать цепочку из таблицы выше.
2. Сохранить отдельные токены для ролей (повторить **Get Token** для каждой роли или завести копии окружения).
3. Держать открытыми: терминал с `docker compose`, Postman с коллекцией, админку, Swagger при необходимости.