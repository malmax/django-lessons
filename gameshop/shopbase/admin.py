from django.contrib import admin
from .models import GameProduct, LanguageCategory, PlatformCategory

# Register your models here.
admin.site.register(GameProduct)
admin.site.register(LanguageCategory)
admin.site.register(PlatformCategory)