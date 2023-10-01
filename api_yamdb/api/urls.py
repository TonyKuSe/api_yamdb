from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    CategoryViewSet, CommentsViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UserSignUpViewSet, UserAuthTokenAPIView, UserModelViewSet
)

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='categories'),
router_v1.register('titles', TitleViewSet, basename='titles'),
router_v1.register('genres', GenreViewSet, basename='genres'),
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router_v1.register('users', UserModelViewSet, basename='users')

auth_v1 = [
    path('signup/', UserSignUpViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('token/', UserAuthTokenAPIView.as_view(),
         name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_v1)),
]
