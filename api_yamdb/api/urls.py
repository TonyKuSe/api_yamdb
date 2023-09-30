from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (CategoryViewSet, CommentsViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet)

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='categories'),
router_v1.register('titles', TitleViewSet, basename='titles'),
router_v1.register('genres', GenreViewSet, basename='genres'),
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
