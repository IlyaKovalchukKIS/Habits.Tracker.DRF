from pprint import pprint
from rest_framework import viewsets, generics

from habits import permissions
from habits.models import Habit
from habits.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        user = User.objects.get(email=data.data.get('email'))
        user.set_password(request.data.get('password'))
        user.save()
        return data

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        user = User.objects.get(email=data.data.get('email'))
        user.set_password(request.data.get('password'))
        user.save()
        return data
