from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_v2

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views_v2

router = DefaultRouter()
router.register(r'trades', views_v2.TradeViewSet, basename='trade')
router.register(
    r'trades/(?P<trade_pk>\d+)/images', 
    views_v2.ImageViewSet, 
    basename='trade-images'
)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_login'),
]