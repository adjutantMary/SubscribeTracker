from django.shortcuts import render
from .models import Tariff, UserSubscription
from .serializers import TariffSerializer, UserSubscriptionSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class TariffView(APIView):
    """Роуты для тарифов"""
    
    permission_classes = (AllowAny, )
    
    def get(self, request):
        """Возвращает список существующих тарифов"""
        tariff_list = Tariff.objects.all()
        serializer = TariffSerializer(tariff_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSubscriptionView(APIView):
    """Роуты для подписок"""
    permission_classes = (AllowAny, )
    
    def get(self, request):
        """Просмотр подписок пользователя"""
        try:
            subscription = UserSubscription.objects.select_related(
                'tariff'
                ).get(user=request.user, is_active=True)
        except UserSubscription.DoesNotExist:
            return Response({"detail": "Подписка не найдена"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Создание подписки"""
        serializer = UserSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """Обновление подписки"""
        try:
            subscription = UserSubscription.objects.get(user=request.user, is_active=True)
        except UserSubscription.DoesNotExist:
            return Response({"detail": "Подписка не найдена."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Удаление подписки"""
        try:
            subscription = UserSubscription.objects.get(user=request.user, is_active=True)
        except UserSubscription.DoesNotExist:
            return Response({"detail": "Подписка не найдена"}, status=status.HTTP_404_NOT_FOUND)
        subscription.is_active = False
        subscription.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
                
            
    



@api_view(['GET'])
def get_tariffs_list(request):
    tariffs = Tariff.objects.all()
    serializer = TariffSerializer(tariffs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_subscriptions(request):
    subscriptions = UserSubscription.objects.all()
    serializer = UserSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user_subscription(request):
    serializer = UserSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
# Create your views here.
