from django import template
from carousel.models import Carousel

register = template.Library()

@register.tag('carousel')
def do_carousel(parser, token):
    """
    {% carousel $carousel_obj %}
    """
    carousel = token.split_contents()[1]
    return CarouselNode(object=carousel)


@register.tag('carousel_with_name')
def do_carousel_with_name(parser, token):
    """
    {% carousel_with_name $carousel_name %}
    """
    carousel_name = token.split_contents()[1]
    return CarouselNode(name=carousel_name)


@register.tag('carousel_with_id')
def do_carousel_with_id(parser, token):
    """
    {% carousel_with_name $carousel_id %}
    """
    carousel_id = token.split_contents()[1]
    return CarouselNode(id=carousel_id)


class CarouselNode(template.Node):
    def __init__(self, object=None, name=None, id=None):
        self.carousel_object = object
        self.carousel_name = name
        self.carousel_id = id
    
    
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
        carousel = self.get_object(context)
        
        context['carousel'] = carousel
        return template.loader.render_to_string('carousel/templatetags/carousel.html', context)
