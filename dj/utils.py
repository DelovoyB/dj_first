import logging


def log_action(logger_name: str, level: str, message: str, **kwargs):
    """
    Универсальная функция для логгирования.

    :param logger_name: Имя логгера (например, 'api').
    :param level: Уровень логирования ('INFO', 'ERROR', 'WARNING', 'DEBUG', 'CRITICAL').
    :param message: Основное сообщение для логгирования.
    :param kwargs: Дополнительные параметры (например, данные контекста).
    """
    logger = logging.getLogger(logger_name)

    # Включаем контекст в лог-сообщение (опционально)
    if kwargs:
        context = ", ".join(f"{key}={value}" for key, value in kwargs.items())
        message = f"{message} | Context: {context}"

    # Логгирование в зависимости от уровня
    level = level.upper()
    if level == 'INFO':
        logger.info(message)
    elif level == 'WARNING':
        logger.warning(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'DEBUG':
        logger.debug(message)
    elif level == 'CRITICAL':
        logger.critical(message)
    else:
        logger.info(f"Unknown level '{level}' provided. Defaulting to INFO: {message}")
