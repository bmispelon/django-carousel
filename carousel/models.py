from itertools import chain, groupby
import random

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils import weighted_shuffle, shuffled

class Carousel(models.Model):
    class DISTRIBUTIONS:
        SEQUENTIAL = 1
        RANDOM = 2
        WEIGHTED_RANDOM = 3
        CLUSTER_RANDOM = 4

        choices = [
            (SEQUENTIAL, _("sequential")),
            (RANDOM, _("random")),
            (WEIGHTED_RANDOM, _("weighted random")),
            (CLUSTER_RANDOM, _("cluster random"))
        ]

    name = models.CharField(_('name'), max_length=50, unique=True)
    distribution = models.PositiveSmallIntegerField(_('distribution'),
                                                    choices=DISTRIBUTIONS.choices,
                                                    default=DISTRIBUTIONS.SEQUENTIAL)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
        ordering = ('name', )

    def get_elements(self, seed=None):
        """
        Returns the list of elements for this carousel.
        The order in which they are returned depends on the `distribution` field.
        """
        if seed is not None:
            random.seed(seed)
        return {
            self.DISTRIBUTIONS.SEQUENTIAL: self._get_elements_sequential,
            self.DISTRIBUTIONS.RANDOM: self._get_elements_random,
            self.DISTRIBUTIONS.WEIGHTED_RANDOM: self._get_elements_weighted_random,
            self.DISTRIBUTIONS.CLUSTER_RANDOM: self._get_elements_cluster_random
        }.get(self.distribution)()

    def _get_elements_sequential(self):
        """
        Elements are sorted according to their `position` attribute.
        """
        return self.elements.order_by('position')

    def _get_elements_random(self):
        """
        Elements are simply shuffled randomly.
        """
        return shuffled(self.elements.all())

    def _get_elements_weighted_random(self):
        """
        Elements are shuffled semi-randomly.
        The `position` attribute of each element act as a weight for the randomization.
        Elements that are "heavier" are more likely to be at the beginning of the list.
        """
        return suffled(elements, weight=lambda e: e.position)

    def _get_elements_cluster_random(self):
        """
        Elements are grouped according to their `position` attribute.
        Each group is then shuffled randomly.
        """
        qs = self.elements.order_by('position')
        grouped = groupby(qs, key=lambda e: e.position)
        return chain.from_iterable(shuffled(elements) for _, elements in grouped)


class CarouselElement(models.Model):
    POSITION_HELP_TEXT = _("The position of the element in the sequence or "
                           "the weight of the element in the randomization "
                           "process (depending on the carousel\'s distribution).")
    carousel = models.ForeignKey(Carousel, verbose_name=_('carousel'),
                                 related_name='elements')
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    url = models.URLField(_('URL'), blank=True)
    position = models.PositiveIntegerField(_('position'), default=1,
                                           help_text=POSITION_HELP_TEXT)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('carousel element')
        verbose_name_plural = _('carousel elements')
        ordering = ('position', 'name')
