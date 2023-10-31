from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateApiView, HabitListApiView, HabitDestroyAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateApiView.as_view(), name='habit_create'),
    path('list/', HabitListApiView.as_view(), name='habit_list'),
    path('destroy/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_destroy'),
    path('retrieve/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update')
]