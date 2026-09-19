from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.user_id}"