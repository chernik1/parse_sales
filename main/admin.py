from django.contrib import admin
from .models import Parser
# Register your models here.

@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'name_company', 'name_purchase', 'date', 'price')
