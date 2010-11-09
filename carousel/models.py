from django.db import models
from django.utils.translation import gettext_lazy as _

class Carousel(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
    
    def get_elements(self):
        return self.elements.all().order_by('name') # TODO: sort according to self.order


class CarouselElement(models.Model):
    carousel = models.ForeignKey(Carousel, verbose_name=_('carousel'), related_name='elements')
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    url = models.URLField(_('URL'), blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('carousel element')
        verbose_name_plural = _('carousel elements')
