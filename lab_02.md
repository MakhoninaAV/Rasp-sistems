
# Лабораторная работа №2
## Клиент-серверные системы. HTTP, веб-серверы и RESTful API

**Вариант 13** | **Выполнила:** Махонина Анна | **Группа:** ЦИБ-241

---

## 1. Цель работы

Изучить методы анализа HTTP-запросов (telnet, curl), освоить настройку Nginx в качестве обратного прокси, применить принципы REST для создания API на Flask.

---

## 2. Краткая теория

- **HTTP** — протокол прикладного уровня. Основные методы: GET (получение), POST (создание), PUT (обновление), DELETE (удаление). Коды состояния: 200 (OK), 201 (создано), 301/307 (редирект), 404 (не найдено).
- **REST** — архитектурный стиль: клиент-сервер, отсутствие состояния, единообразие интерфейса.
- **Nginx** — веб-сервер. В режиме обратного прокси перенаправляет запросы на внутренние серверы (например, Flask), обеспечивая кэширование и безопасность.

---

## 3. Вариант задания (№13)

| Часть | Задание |
|-------|---------|
| 1. HTTP-анализ | Запрос новостей rbc.ru через curl |
| 2. REST API | Трекер задач (id, title, status, assignee) |
| 3. Nginx | Обратный прокси для Flask API |

---

## 4. Выполнение работы

### 4.1. HTTP-анализ rbc.ru

**Команда:**
```bash
curl -v http://rbc.ru 2>&1 | head -40
```

**Результат:**
![HTTP-анализ](https://github.com/MakhoninaAV/-/blob/main/01_HTTP-%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20rbc.ru.png)

**Анализ:** Сервер вернул код `307 Temporary Redirect` с заголовком `Location: https://www.rbc.ru/...`. Это перенаправление с HTTP на HTTPS для безопасности.

---

### 4.2. REST API "Трекер задач" (Flask)

**Листинг app.py:**
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Изучить HTTP", "status": "done", "assignee": "Student"},
    {"id": 2, "title": "Настроить Nginx", "status": "in_progress", "assignee": "Student"}
]
next_id = 3

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    return jsonify(task) if task else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_id
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Title required'}), 400
    new_task = {
        'id': next_id,
        'title': request.json['title'],
        'status': request.json.get('status', 'pending'),
        'assignee': request.json.get('assignee', 'Unknown')
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Запуск Flask:**
![Flask запуск](https://github.com/MakhoninaAV/-/blob/main/02_%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20FLASK.png)

**Тестирование (прямые запросы):**

| Операция | Команда | Результат |
|----------|---------|-----------|
| GET все задачи | `curl http://127.0.0.1:5000/api/tasks` | ![2 задачи](https://github.com/MakhoninaAV/-/blob/main/03_GET%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%20(%D0%92%D1%8B%D0%B2%D0%BE%D0%B4%20JSON%20%D1%81%D0%BE%20%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%BC%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20(2%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8)).png) |
| POST задача | `curl -X POST -H "Content-Type: application/json" -d '{"title": "Сдать лабу", "status": "pending", "assignee": "Me"}' http://127.0.0.1:5000/api/tasks` | ![id 3](https://github.com/MakhoninaAV/-/blob/main/04_POST%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%20(%D0%92%D1%8B%D0%B2%D0%BE%D0%B4%20JSON%20%D1%81%20%D0%BD%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B5%D0%B9%20(id%203)).png) |
| GET после POST | `curl http://127.0.0.1:5000/api/tasks` | ![3 задачи](https://github.com/MakhoninaAV/-/blob/main/05_%D0%94%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8%20(%D0%92%D1%8B%D0%B2%D0%BE%D0%B4%20JSON%20%D1%81%203%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8).png) |

---

### 4.3. Настройка Nginx (обратный прокси)

**Установка и запуск:**
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

![Nginx active](https://github.com/MakhoninaAV/-/blob/main/06_Nginx%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%20%D0%B8%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82(active%20(running)).png)

**Конфигурация** (`/etc/nginx/sites-available/api_proxy`):
```nginx
server {
    listen 80 default_server;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Активация:**
```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/api_proxy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

![Nginx test]()

---

### 4.4. Тестирование через Nginx

| Операция | Команда | Результат |
|----------|---------|-----------|
| GET через Nginx | `curl http://localhost/api/tasks` | ![3 задачи](https://github.com/MakhoninaAV/-/blob/main/07_%20%D0%9A%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%20Nginx.png) |
| POST через Nginx | `curl -X POST -H "Content-Type: application/json" -d '{"title": "Финальный тест", "status": "done", "assignee": "Boss"}' http://localhost/api/tasks` | ![id 4](https://github.com/MakhoninaAV/-/blob/main/08_POST%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20Nginx%20(%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D1%83).png) |
| GET после POST | `curl http://localhost/api/tasks` | ![4 задачи](https://github.com/MakhoninaAV/-/blob/main/09_%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%87%D0%B5%D1%82%D0%B2%D0%B5%D1%80%D1%82%D0%BE%D0%B9%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8.png) |

**Логи Flask (прямые запросы + через Nginx):**
![Логи](https://github.com/MakhoninaAV/-/blob/main/10_%D0%9B%D0%BE%D0%B3%D0%B8%20Flask.png)

Логи подтверждают: все запросы успешно обработаны, запросы через Nginx приходят с `HTTP/1.0`.

---

## 5. Результаты

| Метод | Эндпоинт | Через | Статус |
|-------|----------|-------|--------|
| GET | `/api/tasks` | Flask (5000) | ✅ 200, 2 задачи |
| POST | `/api/tasks` | Flask (5000) | ✅ 201, создана id=3 |
| GET | `/api/tasks` | Flask (5000) | ✅ 200, 3 задачи |
| GET | `/api/tasks` | Nginx (80) | ✅ 200, 3 задачи |
| POST | `/api/tasks` | Nginx (80) | ✅ 201, создана id=4 |
| GET | `/api/tasks` | Nginx (80) | ✅ 200, 4 задачи |

---

## 6. Выводы

В ходе работы:
1. Проведен HTTP-анализ rbc.ru: выявлен редирект 307 на HTTPS.
2. Разработано REST API "Трекер задач" на Flask с поддержкой GET и POST.
3. Настроен Nginx как обратный прокси, все запросы к `/api/` успешно перенаправляются на Flask.
4. Выполнено полное тестирование, система работает стабильно.

**Все требования варианта №13 выполнены. API доступен как напрямую, так и через прокси-сервер Nginx.**

---
