from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CategoryViewSet, TitlesViewSet, GenreViewSet

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='categories'),
router_v1.register('titles', TitlesViewSet, basename='titles'),
router_v1.register('genres', GenreViewSet, basename='genres'),


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
