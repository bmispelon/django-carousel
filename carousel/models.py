import random

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from . import shuffling

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

    _cached_elements = None

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('carousel')
        verbose_name_plural = _('carousels')
        ordering = ('name', )

    def get_elements(self, seed=None, cached=True):
        """
        Returns the list of elements for this carousel.
        The order in which they are returned depends on the `distribution` field.
        """
        if seed is not None:
            random.seed(seed)

        if cached and self._cached_elements is None:
            self._cached_elements = list(self.elements.all())

        elements = self._cached_elements if cached else self.elements.all()

        return self.shuffle(elements)

    @property
    def shuffle(self):
        """
        Return the appropriate shuffle function for this carousel.
        """
        return {
            self.DISTRIBUTIONS.SEQUENTIAL: shuffling.sequential,
            self.DISTRIBUTIONS.RANDOM: shuffling.random,
            self.DISTRIBUTIONS.WEIGHTED_RANDOM: shuffling.weighted_random,
            self.DISTRIBUTIONS.CLUSTER_RANDOM: shuffling.cluster_random,
        }[self.distribution]


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

    @cached_property
    def image_url(self):
        return self.image.url
