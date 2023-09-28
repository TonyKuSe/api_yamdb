from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, TitlesViewSet, GenreViewSet



router_v1 = SimpleRouter()
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
),
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
),
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
),


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
