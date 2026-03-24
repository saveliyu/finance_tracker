# Finance Tracker

Веб приложение для учета своих расходов.

**Сылка на сайт**: https://dashosavo.ru

## 🚀 Функционал

- Добавление и удаление расходов
- Распределение по категориям (еда, транспорт, развлечения и т.д.)
- Фильтрация по дате и пользователю
- Пагинация списка расходов
- Дашборд с отображением трат по категориям
- Доступ только для участников вашей семьи
- Система ролей внутри семьи
- Вход в семью по одноразовому коду

## 🛠️ Технологии

- Python 3.13
- Django
- PostgreSQL
- Docker & Docker Compose
- Nginx
- HTML / CSS 
- Chart.js
- Django Debug Toolbar

## Установка

```bash
git clone https://github.com/saveliyu/finance_tracker
cd finance_tracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

Создайте `.env` файл и укажите необходимые переменные окружения.
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Запуск

```bash
python manage.py runserver
```

Открыть в браузере:

```
http://127.0.0.1:8000/
```

## Структура проекта

```
finance_tracker/
├── base/              # Основное приложение
├── users/             # Приложение Авторизации
├── family/            # Приложение Семьи
├── dashboard/         # Логика Дашборда
├── templates/         # HTML шаблоны
├── static/            # CSS / JS / изображения
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── requirements.txt
├── .env
├── .gitignore
└── manage.py
```

## Тесты

```bash
python manage.py test
```

## 📌 Планы на будущее

- [ ] API (DRF)
- [ ] Автоподгрузка (infinite scroll)
- [ ] Redis для кэширования
- [ ] Экспорт в CSV
- [ ] Telegram-бот для удобного учета расходов

## Обратная связь
Для связи пишите:

Telegram: @tretiviperr