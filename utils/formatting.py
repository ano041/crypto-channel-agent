def safe_md2(text: str) -> str:
    """
    Экранирование специальных символов для MarkdownV2.
    
    Args:
        text: Исходный текст
        
    Returns:
        Экранированный текст, безопасный для MarkdownV2
    """
    if not text:
        return ""
    
    # Символы, которые нужно экранировать в MarkdownV2
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # Проверка на уже экранированные символы
        if char == '\\' and i + 1 < len(text):
            result.append(char)
            result.append(text[i + 1])
            i += 2
            continue
        
        # Экранирование специальных символов
        if char in escape_chars:
            result.append('\\')
        
        result.append(char)
        i += 1
    
    return ''.join(result)


def truncate_text(text: str, max_length: int = 4096, suffix: str = "...") -> str:
    """
    Обрезка текста до максимальной длины с добавлением суффикса.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_tickers(tickers: list[str]) -> str:
    """
    Форматирование списка тикеров для отображения.
    
    Args:
        tickers: Список тикеров
        
    Returns:
        Отформатированная строка с тикерами
    """
    if not tickers:
        return "—"
    
    return " ".join(f"${t.upper()}" for t in tickers if t)
