import logging
from django import template

# Configuración del logger
logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, {})
    except Exception as e:
        logger.error(f"Error getting item: {e}. Dict: {dictionary}, Key: {key}")
        return {}