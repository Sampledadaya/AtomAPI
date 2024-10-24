from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Channel, Message
from .permissions import IsModerator
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, MessageSerializer, ChannelSerializer

# Регистрация пользователя
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'Пользователь успешно зарегистрирован'}, status=status.HTTP_201_CREATED)

# Авторизация пользователя
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Вы успешно вошли в систему'}, status=status.HTTP_200_OK)
    return Response({'error': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)

# Список пользователей и блокировка для модераторов
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsModerator])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'Пользователь заблокирован'})

    @action(detail=True, methods=['post'], permission_classes=[IsModerator])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'Пользователь разблокирован'})

# Работа с каналами
class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer  # Добавляем сериализатор для каналов
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Модератор видит все каналы, обычный пользователь - только те, в которых он состоит
        if user.groups.filter(name='Модератор').exists():
            return Channel.objects.all()
        return user.channels.all()

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        channel = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            channel.members.add(user)
            return Response({'status': 'Пользователь добавлен в канал'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        channel = self.get_object()
        messages = Message.objects.filter(channel=channel)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Сообщение не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)

        channel = self.get_object()
        message = Message.objects.create(
            channel=channel,
            sender=request.user,
            content=content
        )
        return Response({'status': 'Сообщение отправлено'}, status=status.HTTP_201_CREATED)
