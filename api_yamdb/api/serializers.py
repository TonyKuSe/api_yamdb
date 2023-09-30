from rest_framework import serializers
from reviews.models import Category, Comments, Genre, Review, Title
from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'category',
                  'genre', 'name', 'year',
                  'description', 'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'category',
                  'genre', 'name',
                  'year', 'description')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='id',
                                         read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        validators=[UniqueValidator(queryset=Comments.objects.all())])

    class Meta:
        model = Comments
        fields = ('id', 'author', 'text', 'pub_date')
