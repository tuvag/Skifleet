from django.contrib import admin
from .models import Ski, Skitest

class SkiAdmin(admin.ModelAdmin):
    list_display = ("ski_number", "technique", "grind", "brand", "img", "color_tag", "notes", "ski_owner")

class SkitestAdmin(admin.ModelAdmin):
    list_display=("date_of_test", "temprature", "humidity", "location", "snow_type", "notes", "tester")

admin.site.register(Ski,SkiAdmin)
admin.site.register(Skitest, SkitestAdmin)