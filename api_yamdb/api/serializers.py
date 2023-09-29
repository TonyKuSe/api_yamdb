from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Titles


class CategorySerializer(serializers.ModelSerializer):
    
    count = serializers.SerializerMethodField()
    
    class Meta:
        fields = ('id', 'name', 'slug', 'count',)
        read_only_fields = ('id',) 
        model = Category
        lookup_field = 'name'
    
    def get_count(self, obj):
        return Category.objects.all().count()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug',)
        read_only_fields = ('id',) 
        model = Genre
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('category', 'genre', 'name', 'year')
        model = Titles