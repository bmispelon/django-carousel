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
        return self.elements.all()


class CarouselElement(models.Model):
    carousel = models.ForeignKey(Carousel, verbose_name=_('carousel'), related_name='elements')
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    url = models.URLField(_('URL'), blank=True)
    position = models.PositiveIntegerField(_('position'), help_text=_('elements will be displayed in ascending order of position'), default=1)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('carousel element')
        verbose_name_plural = _('carousel elements')
        ordering = ('position', 'name')
