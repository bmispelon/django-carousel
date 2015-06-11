from django import template
from django.core.exceptions import ObjectDoesNotExist
from carousel.models import Carousel

register = template.Library()

@register.inclusion_tag('carousel/templatetags/carousel.html')
def carousel(carousel, max_items=None):
    """
    {% carousel $carousel_obj [max_items] %}
    """
    elements = carousel.get_elements()
    if max_items is not None:
        elements = list(elements)[:max_items]
    return {'elements': elements}


@register.inclusion_tag('carousel/templatetags/carousel.html')
def carousel_with_name(name, max_items=None):
    """
    {% carousel_with_name $carousel_name [max_items] %}
    """
    obj = Carousel.objects.get(name=name)
    return carousel(obj, max_items)


@register.inclusion_tag('carousel/templatetags/carousel.html')
def carousel_with_id(id, max_items=None):
    """
    {% carousel_with_id $carousel_id [max_items] %}
    """
    obj = Carousel.objects.get(pk=id)
    return carousel(obj, max_items)
