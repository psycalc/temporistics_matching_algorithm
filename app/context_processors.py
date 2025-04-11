import os
from flask import current_app, g
from flask_babel import get_locale

def custom_gettext(message):
    """Функція перекладу, яка буде використовуватися у шаблонах."""
    try:
        from flask_babel import gettext as _
        return _(message)
    except Exception as e:
        current_app.logger.error(f"[TRANSLATION] Помилка перекладу: {e}")
        return message

def inject_translation():
    """Додає функцію перекладу в контекст шаблону."""
    locale = str(get_locale())
    current_app.logger.info(f"[CONTEXT] Додаю функцію перекладу для локалі: {locale}")
    
    return {
        'c_': custom_gettext,
        'gettext': custom_gettext,
        'current_locale': locale
    } 