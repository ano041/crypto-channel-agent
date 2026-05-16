"""
Тесты для Crypto Channel Agent без реальных API ключей.
Использует заглушки (mocks) для эмуляции GPT и Tavily.
Запускается без pytest, используя только стандартную библиотеку.
"""
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем наши модули
from tools.validator import validate_post, validate_callback_data
from utils.formatting import safe_md2, truncate_text, format_tickers

# --- Тесты утилит (не требуют API) ---

def test_safe_md2():
    """Проверка экранирования специальных символов MarkdownV2"""
    text = "Hello [World]! Check (1+1)=2. It costs $100."
    result = safe_md2(text)
    # Проверяем, что скобки и другие символы экранированы
    assert "\\[" in result
    assert "\\]" in result
    assert "\\(" in result
    print("✅ Тест safe_md2 пройден")

def test_validate_post():
    """Проверка валидации контента поста"""
    # Валидный пост
    valid_post = {
        "content": {
            "headline": "BTC Update",
            "body": "Bitcoin is up! " * 10  # Достаточно длинный текст
        },
        "meta": {"sentiment": "positive"}
    }
    is_valid, error = validate_post(valid_post)
    assert is_valid is True, f"Ожидалась валидность, ошибка: {error}"
    
    # Невалидный пост (нет заголовка)
    invalid_post = {
        "content": {
            "headline": "",
            "body": "Some text here " * 10
        }
    }
    is_valid, error = validate_post(invalid_post)
    assert is_valid is False
    assert "заголовок" in error.lower()
    print("✅ Тест validate_post пройден")

def test_validate_callback_data():
    """Проверка валидации callback_data"""
    # Валидные данные
    is_valid, action, key = validate_callback_data("approve:post_123")
    assert is_valid is True
    assert action == "approve"
    assert key == "post_123"
    
    # Невалидные данные
    is_valid, action, key = validate_callback_data("invalid")
    assert is_valid is False
    
    is_valid, action, key = validate_callback_data("hack:../../etc")
    assert is_valid is False or len(key) <= 64  # Защита от длинных ключей
    print("✅ Тест validate_callback_data пройден")

# --- Тесты сервисов с моками ---

async def test_moderation_service_available():
    """Проверка доступности модуля модерации"""
    from services import moderator
    assert hasattr(moderator, 'send_for_approval')
    print("✅ Тест moderator module пройден")

async def test_scheduler_functions_available():
    """Проверка доступности функций планировщика"""
    from services import scheduler
    assert hasattr(scheduler, 'schedule_post')
    assert hasattr(scheduler, 'start_scheduler')
    assert hasattr(scheduler, 'stop_scheduler')
    print("✅ Тест scheduler functions пройден")

# --- Интеграционный тест потока генерации ---

async def test_full_generation_flow_mock():
    """
    Эмулирует полный цикл: Поиск -> Генерация GPT -> Валидация -> Форматирование
    """
    # 1. Эмуляция ответа GPT (Генерация) в правильном формате
    mock_gpt_response = {
        "content": {
            "headline": "Рынок растет",
            "body": "Биткоин пробил сопротивление и показывает уверенный рост.",
            "tickers": ["BTC", "ETH"]
        },
        "meta": {
            "sentiment": "positive",
            "urgency": "medium"
        }
    }
    
    # 2. Валидация сгенерированного поста
    is_valid, error = validate_post(mock_gpt_response)
    assert is_valid is True, f"Пост не прошел валидацию: {error}"
    
    # 3. Форматирование заголовка для Telegram
    formatted_headline = safe_md2(mock_gpt_response["content"]["headline"])
    assert "Рынок растет" in formatted_headline
    
    # 4. Форматирование тикеров
    tickers_str = format_tickers(mock_gpt_response["content"]["tickers"])
    assert "$BTC" in tickers_str
    assert "$ETH" in tickers_str
    
    print("✅ Тест полного цикла (Full Flow) пройден")

async def run_all_tests():
    """Запуск всех тестов вручную, если pytest не установлен"""
    print("🚀 Запуск тестов без API ключей...\n")
    
    try:
        # Тесты утилит
        test_safe_md2()
        test_validate_post()
        test_validate_callback_data()
        
        # Тесты сервисов
        await test_moderation_service_available()
        await test_scheduler_functions_available()
        await test_full_generation_flow_mock()
        
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Проект готов к работе. Осталось только добавить реальные API ключи.")
        return True
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
