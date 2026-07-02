from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    """Кастомная модель пользователя"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    
    def __str__(self):
        return self.username

class Trade(models.Model):
    """Объявление"""
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='trades')
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def __str__(self):
        return self.title
    
class Image(models.Model):
    """Изображение поля"""
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='images')
    trade = models.ForeignKey(Trade, 
                              on_delete=models.CASCADE,
                              related_name='images')
    
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Photo for {self.trade.title}"