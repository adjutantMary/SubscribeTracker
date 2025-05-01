from django.db import models
from subscriptions.models import CustomUser


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    class StatusChoices(models.TextChoices):
        NEW = "NEW", "Новый"
        IN_PROGRESS = "IN_PROGRESS", "В обработке"
        DONE = "DONE", "Выполнен"
        CANCELED = "CANCELED", "Отменен"

    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
