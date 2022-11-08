from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TransactionsViewSetFilter
from .models import Category, Transaction, UserProfile
from .serializers import (UserSerializer, CategorySerializer, TransactionSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    Для регистрации нового пользователя: /api/users/
    Для получения access токена(post запрос с username и password): /api/token/


    Для получения профиля пользователя необходимо предьявить access token: /api/users/get_profile/
    Необходимо передать в headers ключ Authorization со значением Bearer access token
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=('get',), detail=False)
    def get_profile(self, request):
        pk = self.request.user.id
        user: User = User.objects.get(pk=pk)
        user_profile: UserProfile = UserProfile.objects.get(user=pk)
        return Response(data={
            'user': user.username,
            'balance': user_profile.balance.amount
        }, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Для доступа к ендпоинтам необходимо предьявить access token
    Необходимо передать в headers ключ Authorization со значением Bearer access token
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
        }


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Для доступа к ендпоинтам необходимо предьявить access token
    Необходимо передать в headers ключ Authorization со значением Bearer access token


    Для того, что бы отсортировать транзакции по времени или сумме нужно передать в url параметр ordering
    и указать поле по которому сортировать(доступно два поля sum, time), например запрос будет выглядеть так:
    /api/transactions/?ordering=sum
    для сортировки по убыванию нужно добавить минус в начале поля:
    /api/transactions/?ordering=-sum


    Так же есть фильтрация по сумме и времени:
    /api/transactions/?time__lte=&time__gte=&sum__lte=&sum__gte=
    time_lte - возвращаеь все транзакции с временем меньше или равным
    time_gte - с больше или равным
    sum_lte - с суммой меньшей или равной
    sum_gte -  с большей или равной
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = TransactionsViewSetFilter
    filter_backends = [SearchFilter, OrderingFilter, filters.DjangoFilterBackend]
    ordering_fields = ('sum', 'time')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
        }
