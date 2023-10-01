from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer, UserAuthTokenSerializer,
    UserSerializer, UserSignUpSerializer
)
from .mixins import BasaModelViewMixin
from reviews.models import Category, Title, Genre
from users.models import EmailVerification


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


class UserSignUpViewSet(viewsets.GenericViewSet):
    """
    Зарегистрировать пользователя. Права доступа: Доступно без токена
    """
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny, )

    def required_fields_not_exist(self, request):
        error_context = {}
        rquired_field_not_found_err = 'Запрос не содержит необходимых данных'
        for field_name in ('username', 'email'):
            if field_name not in request.data:
                error_context[field_name] = [rquired_field_not_found_err]
        return error_context

    def create(self, request):
        required_fields_not_exist = self.required_fields_not_exist(request)
        if required_fields_not_exist:
            return Response(
                required_fields_not_exist, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(
            username=request.data['username'], email=request.data['email']
        )[:1]
        if not user.exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
            )
            verify = EmailVerification.objects.create(
                user=user
            )
        else:
            print(type(user))
            verify = get_object_or_404(EmailVerification, user=user)
        verify.set_new_confirm_code()
        verify.send_verification_email()
        verify.save()
        return Response(request.data, status=status.HTTP_200_OK)


class UserAuthTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = str(RefreshToken.for_user(request.user).access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = self.queryset.get(username=serializer.data['username'])
        verify = EmailVerification.objects.create(
            user=user
        )
        verify.set_new_confirm_code()
        verify.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
