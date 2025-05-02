from django.urls import path
from .views import OrderListCreateView

urlpatterns = [
    path("create-new-order/", OrderListCreateView.as_view(), name="order-list-create"),
]
