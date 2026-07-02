from django.urls import path
from . import views

urlpatterns = [
    # ручки
    path('api/v1/trades/', views.trades_list, name='trades_list'),
    path('api/v1/trades/<int:trade_id>/', views.trade_detail, name='trade_detail'),
    path('api/v1/trades/<int:trade_id>/images/', views.add_image, name='add_image'),
    path('api/v1/trades/<int:trade_id>/images/<int:image_id>/', views.delete_image, name='delete_image'),
    
    # логин и регистрация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]