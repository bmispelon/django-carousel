from django.contrib import admin
from carousel.models import Carousel, CarouselElement

class CarouselAdmin(admin.ModelAdmin):
	pass

class CarouselElementAdmin(admin.ModelAdmin):
	pass

admin.site.register(Carousel, CarouselAdmin)
admin.site.register(CarouselElement, CarouselElementAdmin)
