from django.contrib import admin
from .models import Tariff, UserSubscription


admin.site.register(Tariff)
admin.site.register(UserSubscription)
