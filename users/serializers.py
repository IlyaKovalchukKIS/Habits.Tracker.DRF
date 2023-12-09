from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'chat_id_tg', "password", "first_name", "last_name", "email", "phone", "avatar",)


class UserPublishedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "avatar",)
