from rest_framework import serializers
from reviews.models import Category, Genre, Titles, Review, Comments


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
        fields = ('id', 'category', 'genre', 'name', 'year')
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='id',
                                         read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'author', 'text', 'pub_date')
