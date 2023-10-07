from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import BasaModelViewMixin
from .serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer,
    ReviewSerializer, TitleReadSerializer, TitleWriteSerializer,
    UserAuthTokenSerializer, UserSerializer, UserSignUpSerializer
)
from django.conf import settings
from .permissions import (
    IsAdmin, IsAdminOrReadOnly,
    ReadOrUpdateOnlyMe, AuthorAdminModeratorOrReadOnly, NotUpdateMeRole
)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CategoryViewSet(BasaModelViewMixin):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(BasaModelViewMixin):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsAdminOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Review."""
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & AuthorAdminModeratorOrReadOnly,
    )
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Comments."""
    serializer_class = CommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & AuthorAdminModeratorOrReadOnly,
    )
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                 title__id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


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

    def generate_and_send_code(self, user):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код для получения токена',
            message=f'''
                <p>
                    Для получения токена авторизации в API сервиса api_yamdb
                    отправьте POST-запрос с параметрами username
                    и confirmation_code на эндпоинт <i>/api/v1/auth/token/</i>
                    <br>
                    Ваш код подтверждения:
                    <strong>{confirmation_code}</strong>
                </p>
            ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def create(self, request):
        required_fields_not_exist = self.required_fields_not_exist(request)
        if required_fields_not_exist:
            return Response(
                required_fields_not_exist, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(
            username=request.data['username'], email=request.data['email']
        ).first()
        if not user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
            )
        self.generate_and_send_code(user)
        return Response(request.data, status=status.HTTP_200_OK)


class UserAuthTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if user:
            token = str(RefreshToken.for_user(user).access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(
            {'message': f'There is no user with username {username}'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserModelViewSet(viewsets.ModelViewSet):
    PERSONAL_PATH = 'me'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (
        permissions.IsAuthenticated & ReadOrUpdateOnlyMe & NotUpdateMeRole
        | IsAdmin,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in self.kwargs:
            raise Exception(
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = None
        username = filter_kwargs['pk']
        if username == self.PERSONAL_PATH:
            obj = self.request.user
        else:
            obj = get_object_or_404(queryset, username=username)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, pk=None):
        if pk == self.PERSONAL_PATH:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, pk)
