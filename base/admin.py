from django.contrib import admin
from .models import CustomUser
from .models import *
from django.contrib.auth.admin import UserAdmin
admin.site.register(CustomUser,UserAdmin)
admin.site.register(SamplePack)
admin.site.register(Genere)
admin.site.register(PresetPack)
admin.site.register(Sytheseizer)
admin.site.register(Sample)
admin.site.register(Preset)
admin.site.register(Instrument)
admin.site.register(FavoritePresetPacks)
admin.site.register(FavoriteSamplePacks)
# Register your models here.
