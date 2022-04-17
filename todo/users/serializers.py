from rest_framework.serializers import ModelSerializer

from .models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserStaffModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff')

