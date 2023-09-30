from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response

from api.serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer, ReviewSerializer,
    TitleSerializer, UserSignUpSerializer
)
from api.mixins import BasaModelViewMixin
from reviews.models import Category, Title, Genre


User = get_user_model()


class CategoryViewSet(BasaModelViewMixin):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(BasaModelViewMixin):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserSignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Зарегистрировать пользователя. Права доступа: Доступно без токена
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )

    def create(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
