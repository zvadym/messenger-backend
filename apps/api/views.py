from django.db.models import Q
from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rooms.models import Room
from .serializers import UserSerializer, RoomSerializer
from ..members.models import User


class LoggedInUserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs['pk'])
        except User.DoesNotExist:
            raise Http404


class UserPingView(APIView):
    # Just update "last action" datetime (make user's status == "online")
    def dispatch(self, request, *args, **kwargs):
        request.user.save()
        return Response({'online': True})


class RoomViewMixin:
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(
            Q(is_private=True, members__in=[self.request.user]) |
            Q(is_private=False)
        ).distinct()


class RoomListCreateView(RoomViewMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RoomRetrieveUpdateView(RoomViewMixin, RetrieveUpdateAPIView):
    pass
