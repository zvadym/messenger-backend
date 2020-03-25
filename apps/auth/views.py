from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import RefreshTokenSerializer


class TokenLogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
