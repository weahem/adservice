from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Trade, Image
from .serializers import (
    TradeSerializer, 
    TradeCreateUpdateSerializer,
    ImageSerializer,
    ImageCreateSerializer
)


class TradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для объявлений.
    Поддерживает: list, create, retrieve, update, partial_update, destroy
    """
    queryset = Trade.objects.all()
    permission_classes = [AllowAny]  # <-- без авторизации
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TradeCreateUpdateSerializer
        return TradeSerializer
    
    def get_queryset(self):
        # Если запрос на список (list) - показываем только открытые
        if self.action == 'list':
            return Trade.objects.filter(status=True)
        return Trade.objects.all()


class ImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet для изображений.
    Работает как вложенный ресурс для Trade.
    """
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]  # <-- без авторизации
    
    def get_queryset(self):
        trade_id = self.kwargs.get('trade_pk')
        return Image.objects.filter(trade_id=trade_id)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer
    
    def perform_create(self, serializer):
        trade_id = self.kwargs.get('trade_pk')
        trade = get_object_or_404(Trade, id=trade_id)
        serializer.save(trade=trade)