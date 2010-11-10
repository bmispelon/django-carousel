from django.contrib import admin
from carousel.models import Carousel, CarouselElement

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

class CarouselElementAdmin(admin.ModelAdmin):
    list_display = ('position', 'name', 'url', 'carousel')
    list_display_links = ('name',)
    list_editable = ('position', )

admin.site.register(Carousel, CarouselAdmin)
admin.site.register(CarouselElement, CarouselElementAdmin)
