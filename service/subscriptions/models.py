from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)


class Tariff(models.Model):
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.tariff.name}"
