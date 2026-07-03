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
        # Автор берётся из контекста запроса (передаётся во вьюхе)
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)
    
    def create(self, validated_data):
        
        return super().create(validated_data)