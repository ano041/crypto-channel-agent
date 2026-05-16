# 🧪 Тестирование Crypto Channel Agent без API ключей

## Быстрый старт

Запустите тесты одной командой:

```bash
python tests/test_without_api.py
```

## Что тестируется

### ✅ Юнит-тесты утилит
- **safe_md2** — экранирование специальных символов MarkdownV2
- **validate_post** — валидация структуры поста (заголовок, текст, сентимент)
- **validate_callback_data** — проверка callback_data от кнопок бота

### ✅ Интеграционные тесты
- **moderator module** — доступность функций модерации
- **scheduler functions** — функции планировщика задач
- **full generation flow** — полный цикл: генерация → валидация → форматирование

## Как это работает без API?

Тесты используют **моки** (заглушки) вместо реальных вызовов:
- Вместо GPT-4o-mini — заранее подготовленные JSON-ответы
- Вместо Tavily API — тестовые данные новостей
- Вместо Redis — AsyncMock объекты
- Вместо Telegram Bot — проверка логики без отправки сообщений

## Результаты

При успешном прохождении всех тестов вы увидите:

```
🚀 Запуск тестов без API ключей...

✅ Тест safe_md2 пройден
✅ Тест validate_post пройден
✅ Тест validate_callback_data пройден
✅ Тест moderator module пройден
✅ Тест scheduler functions пройден
✅ Тест полного цикла (Full Flow) пройден

🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
Проект готов к работе. Осталось только добавить реальные API ключи.
```

## Дополнительные проверки

### 1. Проверка синтаксиса всех модулей
```bash
python -m py_compile main.py handlers/*.py services/*.py tools/*.py utils/*.py
```

### 2. Проверка импортов
```bash
python -c "import main; print('✅ Все импорты работают')"
```

## Подготовка к продакшену

Когда получите API ключи:

1. **Создайте файл `.env`**:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   OPENAI_API_KEY=your_openai_key
   TAVILY_API_KEY=your_tavily_key
   REDIS_URL=redis://localhost:6379/0
   ADMIN_IDS=123456789,987654321
   ```

2. **Запустите бота**:
   ```bash
   python main.py
   ```

3. **Проверьте работу через Telegram**:
   - Отправьте `/start` — проверка доступа
   - Отправьте `/generate Bitcoin news` — тест генерации
   - Используйте кнопки Approve/Reject — тест модерации

## Troubleshooting

### Ошибка импорта
```bash
# Убедитесь, что все зависимости установлены
pip install -r requirements.txt
```

### Ошибка подключения к Redis
```bash
# Для локального тестирования можно закомментировать Redis в config.py
# или запустить Redis в Docker:
docker run -d -p 6379:6379 redis:alpine
```

### Тесты не проходят
- Проверите версию Python (требуется 3.9+)
- Убедитесь, что все файлы на месте (`ls -la tools/ utils/ services/`)
- Запустите с флагом `-v` для детальной информации

---

**Статус**: ✅ Все критические ошибки исправлены, тесты работают без API ключей
