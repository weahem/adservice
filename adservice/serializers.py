from rest_framework import serializers
from .models import Trade, Image, User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'created', 'updated', 'image', 'author', 'trade')
        read_only_fields = ('author', 'trade')


class TradeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)  # показывает username вместо id
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Trade
        fields = (
            'id', 'title', 'text', 'status', 
            'created', 'updated', 
            'author', 'author_id', 'images'
        )
        read_only_fields = ('author', 'created', 'updated', 'author_id')


class TradeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('title', 'text', 'status')
    
    def create(self, validated_data):
        # Если пользователь авторизован — ставим его автором
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        else:
            # Если не авторизован — создаём анонимного автора (или можно вернуть ошибку)
            # Для простоты — берём первого пользователя или создаём
            from django.contrib.auth import get_user_model
            User = get_user_model()
            anonymous_user, _ = User.objects.get_or_create(
                username='anonymous',
                defaults={'email': 'anonymous@example.com'}
            )
            validated_data['author'] = anonymous_user
        return super().create(validated_data)


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)
    
    def create(self, validated_data):
        trade_id = self.context['view'].kwargs.get('trade_pk')
        validated_data['trade_id'] = trade_id
        
        # Автор — текущий пользователь или аноним
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['author'] = request.user
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            anonymous_user, _ = User.objects.get_or_create(
                username='anonymous',
                defaults={'email': 'anonymous@example.com'}
            )
            validated_data['author'] = anonymous_user
        
        return super().create(validated_data)