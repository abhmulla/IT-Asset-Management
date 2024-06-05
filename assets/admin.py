from django.contrib import admin
from .models import Asset, AssetType

# Register your models here.

admin.site.register(Asset)
@admin.register(AssetType)
class ModelNameAdmin(admin.ModelAdmin):
    pass

