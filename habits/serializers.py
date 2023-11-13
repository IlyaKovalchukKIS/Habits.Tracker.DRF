from rest_framework import serializers

from habits.models import Habit
from habits.validators import RelatedHabitsValidator, NotNullValidator, MaxTimeToCompleteValidator
from users.serializers import UserPublishedSerializer


class HabitSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitsValidator(related_habit='related_habit', award='award', pleasant_habit='pleasant_habit'),
            NotNullValidator(related_habit='related_habit', award='award', pleasant_habit='pleasant_habit'),
            MaxTimeToCompleteValidator(time_to_complete='time_to_complete')
        ]


class HabitPublishedSerializer(serializers.ModelSerializer):
    user = UserPublishedSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
