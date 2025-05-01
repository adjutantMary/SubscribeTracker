from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order
from .serializers import OrderSerializer
from django.conf import settings

import requests


class OrderListCreateView(APIView):
    """Роуты для работы с заказами"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Получаем все заказы"""
        orders = Order.objects.filter(user=request.user).select_related("user")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создаем новый заказ и отправляем уведомление в бота"""
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            user = request.user
            if user.telegram_id:
                send_telegram_message(user.telegram_id, "Вам пришёл новый заказ!")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """Роут для детализации информации по заказам"""

    permission_classes = (permissions.AllowAny,)

    def get_object(self, user, pk):
        return Order.objects.select_related("user").get(pk=pk, user=user)

    def get(self, request, pk):
        """Получаем заказы конкретного пользователя"""
        try:
            order = self.get_object(request.user, pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        """Обновляем заказ пользователя по его pk"""
        try:
            order = self.get_object(request.user, pk)
            serializer = OrderSerializer(
                order, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        """Удалаем заказ по pk"""
        try:
            order = self.get_object(request.user, pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND
            )


def send_telegram_message(telegram_id, text):
    """Утилита для отправки месседжа"""
    token = settings.TG_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": telegram_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=3)
    except requests.RequestException as e:
        print(f"Ошибка отправки Telegram-сообщения: {e}")
