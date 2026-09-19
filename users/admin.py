from django.contrib import admin
from .models import TelegramUser

# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_id', 'name', 'nickname', 'count', 'is_banned')

    readonly_fields = ('created_at', 'user_id', 'name', 'nickname', 'count', )