from django.contrib import admin
from .models import Ski, Setting, Technique, SkiTest

class SkiAdmin(admin.ModelAdmin):
    list_display = ("ski_number", "technique", "grind", "brand", "img", "color_tag", "notes", "ski_owner")

class SettingAdmin(admin.ModelAdmin):
    list_display=("date", "temprature", "humidity", "location", "snow_type", "notes", "tester")


admin.site.register(Ski,SkiAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Technique)
admin.site.register(SkiTest)