from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, verbose_name='Name')
    nickname = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nickname')
    count = models.PositiveIntegerField(default=0, verbose_name='The number of videos converted into video notes.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Registered')
    is_banned = models.BooleanField(default=False, verbose_name='Banned')



    class Meta:
        verbose_name_plural = "Telegram users"


    def __str__(self):
        return f"{self.name} - {self.user_id}"