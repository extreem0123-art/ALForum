# ALFA LIGHT FORUM 2026

Telegram бот и веб-приложение для конференции ALFA LIGHT FORUM 2026.

## Особенности

- 🤖 Telegram бот с WebApp интеграцией
- 📅 Динамическое расписание мероприятий
- 👥 Спикеры с подробной информацией
- ❓ Часто задаваемые вопросы (FAQ)
- 🗺️ Карта и информация о месте проведения
- 🎨 Современный дизайн с темной темой
- 📱 Адаптивный интерфейс
- 🔒 Безопасная архитектура с переменными окружения

## Технологии

- **Python** - Telegram бот
- **HTML/CSS/JavaScript** - Веб-приложение
- **Telegram WebApp** - Интеграция с Telegram
- **JSON** - Хранение данных
- **Vercel** - Хостинг веб-приложения

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/extreem0123-art/ALForum.git
cd ALForum
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните `.env` файл своими значениями:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
WEBAPP_URL=https://ваш-домен.com
DEBUG=false
```

### 4. Запуск бота

```bash
python bot.py
```

## Деплой на Vercel

Проект настроен для автоматического деплоя на Vercel.

### Автоматический деплой

1. Зарегистрируйтесь на [Vercel](https://vercel.com)
2. Нажмите "Add New..." -> "Project"
3. Импортируйте репозиторий `extreem0123-art/ALForum`
4. Нажмите "Deploy"

Vercel автоматически определит конфигурацию из `vercel.json` и задеплоит приложение.

### Ручной деплой через Vercel CLI

```bash
npm i -g vercel
vercel login
vercel --prod
```

### Структура файлов для Vercel

```
ALForum/
├── vercel.json              # Конфигурация Vercel
├── bot.py                   # Telegram бот (локальный запуск)
├── config/                  # Конфигурация
│   ├── __init__.py
│   └── settings.py
├── static/                  # Статические файлы (деплоятся на Vercel)
│   ├── index.html          # Главная страница
│   ├── data/               # JSON данные
│   │   ├── schedule.json
│   │   ├── speakers.json
│   │   ├── faq.json
│   │   └── venue.json
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── app.js
├── requirements.txt
├── .env.example
└── .gitignore
```

## Конфигурация

### Переменные окружения

- `TELEGRAM_BOT_TOKEN` - Токен вашего Telegram бота
- `WEBAPP_URL` - URL вашего веб-приложения (после деплоя на Vercel)
- `DEBUG` - Режим отладки (true/false)

### Настройка URL в боте

После деплоя на Vercel, обновите URL в `bot.py`:

```python
WEB_APP_URL = "https://ваш-проект.vercel.app"
```

Или используйте переменную окружения:

```python
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://ваш-проект.vercel.app")
```

## Разработка

### Добавление новых спикеров

Отредактируйте `static/data/speakers.json`:

```json
{
  "id": 10,
  "name": "Имя Фамилия",
  "company": "Должность, Компания",
  "badge": "Особая метка",
  "featured": false,
  "topics": ["Тема 1", "Тема 2"],
  "avatar": "URL_аватара_или_dicebear_генератор"
}
```

### Добавление мероприятий

Отредактируйте `static/data/schedule.json`:

```json
{
  "time": "10:00",
  "type": "talk",
  "title": "Название доклада",
  "room": "Зал A",
  "speaker": {
    "name": "Имя Спикера",
    "company": "Компания"
  }
}
```

## Безопасность

- Токен бота хранится в переменных окружения
- Данные отделены от кода
- Реализована валидация окружения Telegram WebApp
- Добавлено логирование и обработка ошибок

## Лицензия

Этот проект распространяется под лицензией MIT.

## Автор

extreem0123-art
