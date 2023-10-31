from rest_framework import serializers

from habits.models import Habit
from habits.validators import RelatedHabitsValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitsValidator(related_habit='related_habit', award='award', pleasant_habit='pleasant_habit')]


# class HabitListSerializer(serializers.ModelSerializer):
#     pleasant_habits_list = HabitCreateSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Habit
#         fields = '__all__'
