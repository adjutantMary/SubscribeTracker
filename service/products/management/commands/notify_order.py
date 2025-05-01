from django.core.management.base import BaseCommand
from subscriptions.models import CustomUser  # подстрой под своё имя приложения
import requests

BOT_URL = "http://telegram_bot:8001/send"


class Command(BaseCommand):
    help = "Уведомление пользователя о новом заказе"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int)

    def handle(self, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = CustomUser.objects.get(id=user_id)

        if not user.telegram_id:
            self.stdout.write("У пользователя не указан Telegram ID")
            return

        message = "Вам пришёл новый заказ!"
        try:
            response = requests.post(
                BOT_URL,
                json={"telegram_id": user.telegram_id, "message": message},
                timeout=3,
            )
            if response.ok:
                self.stdout.write(f"Сообщение отправлено: {message}")
            else:
                self.stderr.write(f"Ошибка отправки: {response.status_code}")
        except requests.RequestException as e:
            self.stderr.write(f"Ошибка запроса: {e}")
