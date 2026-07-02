from django.contrib import admin
from .models import User, Trade, Image

# Register your models here.

# Регистрируем кастомную модель пользователя
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_active')

# Регистрируем модель объявления
@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'created', 'updated')
    list_filter = ('status', 'created')
    search_fields = ('title', 'text', 'author__username')
    readonly_fields = ('created', 'updated')  # поля, которые нельзя редактировать
    fields = ('title', 'text', 'author', 'status', 'created', 'updated')

# Регистрируем модель изображения
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'trade', 'author', 'created')
    list_filter = ('created',)
    search_fields = ('trade__title', 'author__username')
    readonly_fields = ('created', 'updated')