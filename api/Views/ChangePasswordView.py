from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.Serializers import ChangePasswordSerializer


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        """ Change user password"""
        serializer = self.serializer_class(data=self.request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = request.user.json(request)
        return Response(data=response, status=status.HTTP_200_OK)
