from pprint import pprint

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublishedSerializer
from users.models import User


class HabitCreateApiView(generics.CreateAPIView):
    """Создание приывчки"""
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListApiView(generics.ListAPIView):
    """Просмотр списка приывчек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    # permission_classes = [permissions.IsAuthenticated, IsOwner]
    # pagination_class = HabitPaginator

    # def get_serializer_context(self):
    #     queryset = super().get_serializer_context()
    #     print(self.queryset)
    #     q = []
    #     for i in queryset:
    #         print(i)
    #         if not i == self.request.user:
    #             queryset.pop(i)
    #     return queryset


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление приывчки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотр привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Изменение привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitPublishedListAPIView(generics.ListAPIView):
    """Просмотр публичных привычек пользователей"""
    serializer_class = HabitPublishedSerializer
    queryset = Habit.objects.filter(is_published=True)
