from django import template
from core.models import Item

register = template.Library()

@register.filter
def in_category(things, category):
    try:
        category = str(category)
        return Item.objects.filter(category=category)
    except Exception as e:
        print(e)
        print(category)
        return Item.objects.all()