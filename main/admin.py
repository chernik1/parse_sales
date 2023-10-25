from django.contrib import admin
from .models import Parser, ParserDelete
# Register your models here.

@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'name_company', 'name_purchase', 'date', 'price', 'payer_number')

    actions = ['delete_parser_data']

    @admin.action(description='Delete all selected items')
    def delete_parser_data(self, request, queryset):
        queryset.delete()

@admin.register(ParserDelete)
class ParserDeleteAdmin(admin.ModelAdmin):
    list_display = ['id_purchase']