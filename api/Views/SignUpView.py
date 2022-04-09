from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from api.Serializers import SignUpSerializer


class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        """ Create new user as admin user or normal user is_admin True for admin user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()

        # generate token
        token_instance = Token.objects.create(user=user_instance)
        token_instance.generate_key()
        token_instance.save()

        response = serializer.data
        response['status'] = 'SIGN_UP'
        return Response(data=response, status=status.HTTP_201_CREATED)
