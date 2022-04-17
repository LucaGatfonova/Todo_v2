from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer, UserStaffModelSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return UserStaffModelSerializer
        return UserStaffModelSerializer
