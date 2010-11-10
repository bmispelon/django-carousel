from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from utils import weighted_shuffle
from collections import defaultdict

class Carousel(models.Model):
    DISTRIB_SEQUENTIAL = 1
    DISTRIB_RANDOM = 2
    DISTRIB_WEIGHTED_RANDOM = 3
    DISTRIB_CLUSTER_RANDOM = 4
    DISTRIBUTIONS = (
        (DISTRIB_SEQUENTIAL, _('sequential')),
        (DISTRIB_RANDOM, _('random')),
        (DISTRIB_WEIGHTED_RANDOM, _('weighted random')),
        (DISTRIB_CLUSTER_RANDOM, _('cluster random'))
    )
    name = models.CharField(_('name'), max_length=50, unique=True)
    distribution = models.PositiveSmallIntegerField(_('distribution'), choices=DISTRIBUTIONS, default=DISTRIB_SEQUENTIAL)
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
        ordering = ('name', )
    
    def get_elements(self):
        return {
            self.DISTRIB_SEQUENTIAL: self._get_elements_sequential,
            self.DISTRIB_RANDOM: self._get_elements_random,
            self.DISTRIB_WEIGHTED_RANDOM: self._get_elements_weighted_random,
            self.DISTRIB_CLUSTER_RANDOM: self._get_elements_cluster_random
        }.get(self.distribution)()
    
    def _get_elements_sequential(self):
        return self.elements.order_by('position')
    
    def _get_elements_random(self):
        elements = list(self.elements.all()) # force evaluation of queryset
        random.shuffle(elements)
        return elements
    
    def _get_elements_weighted_random(self):
        elements = list(self.elements.all()) # force evaluation of queryset
        weighted_shuffle(elements, key_weight=lambda e: e.position)
        return elements
    
    def _get_elements_cluster_random(self):
        clusters = defaultdict(list)
        for item in self.elements.all():
            clusters[item.position].append(item)
        for cluster in clusters.values():
            random.shuffle(cluster)
        
        sorted_tuples = sorted(clusters.items(), key=lambda t: t[0])
        return reduce(lambda x,t: x + t[1], sorted_tuples, [])


class CarouselElement(models.Model):
    POSITION_HELP_TEXT = _('The position of the element in the sequence or the weight of the element in the randomization process (depending on the carousel\'s distribution).')
    carousel = models.ForeignKey(Carousel, verbose_name=_('carousel'), related_name='elements')
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    url = models.URLField(_('URL'), blank=True)
    position = models.PositiveIntegerField(_('position'), default=1, help_text=POSITION_HELP_TEXT)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('carousel element')
        verbose_name_plural = _('carousel elements')
        ordering = ('position', 'name')
