import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from subscriptions.models import UserSubscription, CustomUser


class ActiveSubscriptionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith("/api/orders/") or request.method != "POST":
            return None
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
        except Exception as e:
            print("[middleware] Ошибка чтения body:", e)
            return JsonResponse({"detail": "Неверный формат запроса"}, status=400)

        if not user_id:
            return JsonResponse({"detail": "user_id не передан"}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"detail": "Пользователь не найден"}, status=404)

        has_active = UserSubscription.objects.filter(user=user, is_active=True).exists()
        if not has_active:
            print("[middleware] Подписка отсутствует")
            return JsonResponse({"detail": "Нет активной подписки"}, status=403)

        return None
