from django.contrib import admin
from .models import Tariff, UserSubscription, CustomUser

admin.site.register(CustomUser)
admin.site.register(Tariff)
admin.site.register(UserSubscription)
