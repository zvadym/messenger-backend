from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rooms.models import Room
from .serializers import UserSerializer, RoomSerializer
from ..members.models import User


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserPingView(APIView):
    def post(self, request):
        request.user.save()
        return Response({'last_action_dt': request.user.last_action_dt})