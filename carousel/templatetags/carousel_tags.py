from django.utils.lru_cache import lru_cache
from django import template

from carousel.models import Carousel

register = template.Library()

@lru_cache(maxsize=None)
def _get_carousel(**kwargs):
    try:
        return Carousel.objects.get(**kwargs)
    except Carousel.DoesNotExist:
        return None


@register.inclusion_tag('carousel/templatetags/carousel.html')
def carousel(carousel=None, name=None, pk=None, max_items=None, size=True):
    assert len([x for x in (carousel, name, pk) if x is not None]) == 1, "You must provide exactly one of (carousel, name, pk)"

    if pk is not None:
        carousel = _get_carousel(pk=pk)
    elif name is not None:
        carousel = _get_carousel(name=name)

    elements = carousel.get_elements() if carousel else []
    if max_items is not None:
        elements = elements[:max_items]

    return {'elements': elements, 'size': size}
