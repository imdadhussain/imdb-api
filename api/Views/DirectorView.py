from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from api.Serializers import DirectorSerializer
from api.models import Director
from api.permissions import IsAdmin


class DirectorView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = DirectorSerializer
    permission_classes = (IsAdmin, IsAuthenticated,)

    def post(self, request):
        try:
            serializer = DirectorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                response['msg'] = "Director created successful."
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                msg = errors[list(errors.keys())[0]][0]
                return Response(data={"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"msg": "Something went wrong. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, director_id):
        error_message = None
        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist as e:
            error_message = "Director Not Found"
        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = DirectorSerializer(data=request.data, instance=director)
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                response['msg'] = "Director updated successful."
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                msg = errors[list(errors.keys())[0]][0]
                return Response(data={"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"msg": "Something went wrong. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, director_id):
        error_message = None
        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist as e:
            error_message = "Director Not Found"
        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)
        director.delete()

        return Response({"msg": "Director deleted successful."}, status=status.HTTP_204_NO_CONTENT)


class DirectorListView(ListAPIView):
    """Handle reading Directors"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
