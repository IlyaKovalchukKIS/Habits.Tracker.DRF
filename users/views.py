from pprint import pprint

from django.shortcuts import render
from django_celery_beat.models import PeriodicTask
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
