from django.urls import path
from .views import TariffView, UserSubscriptionView

urlpatterns = [
    path('tariffs/', TariffView.as_view(), name='tariff-list'),
    path('my/', UserSubscriptionView.as_view(), name='user-subscription'),
]