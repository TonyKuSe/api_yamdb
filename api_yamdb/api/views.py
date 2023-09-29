from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from api.serializers import (CategorySerializer,
                             GenreSerializer, TitlesSerializer,
                             ReviewSerializer, CommentsSerializer)
from api.mixins import BasaModelViewMixin
from reviews.models import Category, Titles, Genre
from .permissions import IsAuthorOrUserOrModerator


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


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Titles.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrUserOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrUserOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
