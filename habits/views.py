from django.shortcuts import render
from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer


class HabitCreateApiView(generics.CreateAPIView):
    """Создание приывчки"""
    serializer_class = HabitSerializer


class HabitListApiView(generics.ListAPIView):
    """Просмотр списка приывчек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление приывчки"""
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Изменение привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
