import logging
from django import template

logger = logging.getLogger(__name__)
register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    try:
        return getattr(obj, attr_name, "")
    except Exception as e:
        logger.error(f"Error getting attribute: {e}. Object: {obj}, Attribute: {attr_name}")
        return ""

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, {})
    except Exception as e:
        logger.error(f"Error getting item: {e}. Dict: {dictionary}, Key: {key}")
        return {}