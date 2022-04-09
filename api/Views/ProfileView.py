from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.models import User
from api.Serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = ProfileSerializer

    def post(self, request):
        user = request.user
        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response(data={"msg": "User Not Found!."}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ProfileSerializer(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                response = user.json(request)
                response['msg'] = "Profile updated successful."
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                msg = errors[list(errors.keys())[0]][0]
                return Response(data={"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"msg": "Something went wrong. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response(data={"msg": "User Not Found!."}, status=status.HTTP_404_NOT_FOUND)

        response = user.json(request)
        return Response(data=response, status=status.HTTP_200_OK)
