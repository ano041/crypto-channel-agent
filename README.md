# Crypto Channel Agent

Автономный AI-агент для генерации и модерации контента в Telegram-канале о криптовалюте.

## Структура проекта

```
crypto-channel-agent/
├── main.py
├── config.py
├── prompts/
├── services/
├── tools/
├── handlers/
├── memory/
├── utils/
├── .env.example
├── requirements.txt
└── README.md
```

## Как запустить

1. `git clone https://github.com/ano041/crypto-channel-agent.git`
2. `cd crypto-channel-agent`
3. `python -m venv venv && source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `cp .env.example .env` и заполните переменные
6. `python main.py`

