from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from subscriptions.models import UserSubscription
from datetime import date
from django.http import JsonResponse


class ActiveSubscriptionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = resolve(request.path_info).route
        if not path.startswith("orders/"):
            return None
        try:
            subscription = UserSubscription.objects.get(
                user=request.user, is_active=True
            )
            return None
        except UserSubscription.DoesNotExist:
            return JsonResponse({"detail": "Нет активной подписки"}, status=403)
