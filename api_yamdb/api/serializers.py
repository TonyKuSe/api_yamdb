from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Category, Comments, Genre, Review, Title
from rest_framework.validators import UniqueValidator
from users.models import EmailVerification


User = get_user_model()


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


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year')
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


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=254
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=150
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if username and email:
            if username == 'me':
                raise serializers.ValidationError(
                    'Нельзя выбрать имя пользователя "me"'
                )
            return super().validate(attrs)
        else:
            raise serializers.ValidationError(
                'Запрос не содержит необходимых данных'
            )


class UserAuthTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )

    def validate(self, attrs):
        verify = get_object_or_404(
            EmailVerification,
            user__username=attrs['username'],
        )
        if verify.confirmation_code == attrs['confirmation_code']:
            return super().validate(attrs)
        else:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле или оно некорректно'
            )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
