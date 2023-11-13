from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublishedSerializer
from users.models import User


class HabitCreateApiView(generics.CreateAPIView):
    """Создание приывчки"""
    serializer_class = HabitSerializer


class HabitListApiView(generics.ListAPIView):
    """Просмотр списка приывчек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    # pagination_class = HabitPaginator


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление приывчки"""
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Изменение привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitPublishedListAPIView(generics.ListAPIView):
    """Просмотр публичных привычек пользователей"""
    serializer_class = HabitPublishedSerializer
    queryset = Habit.objects.filter(is_published=True)
