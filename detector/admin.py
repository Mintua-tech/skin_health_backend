from django.contrib import admin
from .models import SkinDisease

@admin.register(SkinDisease)
class SkinDiseaseAdmin(admin.ModelAdmin):
    # This makes the admin list look like a professional table
    list_display = ('name', 'description', 'cause')
    search_fields = ('name',)