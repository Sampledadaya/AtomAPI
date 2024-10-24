from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat_app.views import register, login_view, UserViewSet, ChannelViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'channels', ChannelViewSet, basename='channel')

urlpatterns = [
    path('api/register/', register, name='register'),  # Регистрация пользователя
    path('api/login/', login_view, name='login'),  # Логин пользователя
    path('api/', include(router.urls)),  # Основные API роуты
]
