from django import template
from django.core.exceptions import ObjectDoesNotExist
from carousel.models import Carousel

register = template.Library()

@register.tag('carousel')
def do_carousel(parser, token):
    """
    {% carousel $carousel_obj [max_items] %}
    """
    bits = token.split_contents()
    carousel = bits[1]
    max_items = bits[2] if len(bits) > 2 else None
    return CarouselNode(object=carousel, max_items=max_items)


@register.tag('carousel_with_name')
def do_carousel_with_name(parser, token):
    """
    {% carousel_with_name $carousel_name [max_items] %}
    """
    bits = token.split_contents()
    carousel_name = bits[1]
    max_items = bits[2] if len(bits) > 2 else None
    return CarouselNode(name=carousel_name, max_items=max_items)


@register.tag('carousel_with_id')
def do_carousel_with_id(parser, token):
    """
    {% carousel_with_name $carousel_id [max_items] %}
    """
    bits = token.split_contents()
    carousel_id = bits[1]
    max_items = bits[2] if len(bits) > 2 else None
    return CarouselNode(id=carousel_id, max_items=max_items)


class CarouselNode(template.Node):
    def __init__(self, object=None, name=None, id=None, max_items=None):
        self.carousel_object = object
        self.carousel_name = name
        self.carousel_id = id
        self.max_items = max_items
    
    
    def get_object(self, context):
        """
        Retrieves the object from the database according to the context.
        """
        obj, name, id = self.carousel_object, self.carousel_name, self.carousel_id
        
        if obj is not None:
            return template.Variable(obj).resolve(context)
        
        if name is not None:
            if name[0] == name[-1] and name[0] in ('"', "'"):
                name = name[1:-1]
            else: # a template variable was given
                name = template.Variable(name).resolve(context)
            return Carousel.objects.get(name=name)
        
        try:
            id = int(id)
        except ValueError:
            id = template.Variable(id).resolve(context)
        return Carousel.objects.get(pk=id)
    
    def render(self, context):
        try:
            carousel = self.get_object(context)
        except ObjectDoesNotExist:
            return ''
        
        elements = carousel.get_elements()
        if self.max_items:
            max_items = template.Variable(self.max_items).resolve(context)
            elements = elements[:max_items]
        context['elements'] = elements
        return template.loader.render_to_string('carousel/templatetags/carousel.html', context)
