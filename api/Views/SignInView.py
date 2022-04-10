from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.auth import password_auth
from api.models import User


class SignInView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if not any([email, password]):
            return Response(data={"msg": "Request Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={"msg": "Invalid Email Id."}, status=status.HTTP_404_NOT_FOUND)
        password_valid = password_auth(user, password)
        if password_valid:
            user_data = user.json(request)
            user_data['status'] = 'SIGN_IN'
            user_data['token'] = {'Token': str(user.auth_token)}

            return Response(data=user_data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": "Invalid Password"}, status=status.HTTP_403_FORBIDDEN)
