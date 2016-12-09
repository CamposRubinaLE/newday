from rest_framework import serializers
from .models import Category, Place, Event

__author__ = 'lucaru9'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class PlaceOfUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'file_1')


class EventSerializer(serializers.ModelSerializer):
    image_category = serializers.ImageField(source='category.image', read_only=True)
    is_qualified = serializers.SerializerMethodField(read_only=True)
    place = serializers.CharField(source='place.name', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_hour', 'end_hour', 'min_price', 'image_1', 'image_category', 'is_qualified',
                  'score', 'place')

    def get_is_qualified(self, obj):
        band = False
        if self.context.get('request').user:
            user = self.context.get('request').user
            if user.is_authenticated():
                for score in obj.scores:
                    if user.id == score.get('id'):
                        band = score.get('val')
        return band


class PlaceSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField(read_only=True)
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'longitude', 'latitude', 'file_1', 'file_2', 'file_3', 'description',
                  'is_favorite', 'events')

    def get_is_favorite(self, obj):
        band = False
        if self.context.get('request').user:
            user = self.context.get('request').user
            if user.is_authenticated():
                if obj.pk in user.places:
                    band = True
        return band
