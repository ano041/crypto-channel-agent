from prompts.schemas import CryptoPostSchema
from utils.logger import logger


def validate_post(post: dict) -> tuple[bool, str]:
    """
    Валидация структуры поста перед публикацией.
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    try:
        if not post:
            return False, "Пост пустой"
        
        content = post.get("content", {})
        if not content:
            return False, "Отсутствует содержимое поста"
        
        headline = content.get("headline", "").strip()
        if not headline:
            return False, "Отсутствует заголовок"
        
        body = content.get("body", "").strip()
        if not body:
            return False, "Отсутствует текст поста"
        
        if len(headline) > 200:
            return False, f"Заголовок слишком длинный ({len(headline)} символов)"
        
        if len(body) < 50:
            return False, f"Текст поста слишком короткий ({len(body)} символов)"
        
        tickers = content.get("tickers", [])
        if tickers and not isinstance(tickers, list):
            return False, "Тикеры должны быть списком"
        
        meta = post.get("meta", {})
        sentiment = meta.get("sentiment", "")
        if sentiment and sentiment not in ["positive", "negative", "neutral"]:
            return False, f"Некорректный сентимент: {sentiment}"
        
        urgency = meta.get("urgency", "")
        if urgency and urgency not in ["low", "medium", "high"]:
            return False, f"Некорректная срочность: {urgency}"
        
        return True, ""
    
    except Exception as e:
        logger.error("Validation error", error=str(e))
        return False, f"Ошибка валидации: {str(e)}"


def validate_callback_data(callback_data: str) -> tuple[bool, str, str]:
    """
    Валидация callback_data от кнопок.
    
    Returns:
        tuple: (is_valid: bool, action: str, post_key: str)
    """
    if not callback_data or ":" not in callback_data:
        return False, "", ""
    
    parts = callback_data.split(":", 1)
    if len(parts) != 2:
        return False, "", ""
    
    action, post_key = parts
    
    if action not in ["approve", "edit", "reject"]:
        return False, "", ""
    
    if not post_key or len(post_key) > 64:
        return False, "", ""
    
    return True, action, post_key
