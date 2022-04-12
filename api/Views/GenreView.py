from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from api.Serializers import GenreSerializer
from api.models import Genre
from api.permissions import IsAdmin


class GenreView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin, IsAuthenticated,)

    def post(self, request):
        try:
            serializer = GenreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                response['msg'] = "Genre created successful."
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                msg = errors[list(errors.keys())[0]][0]
                return Response(data={"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"msg": "Something went wrong. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, genre_id):
        error_message = None
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist as e:
            error_message = "Genre Not Found"
        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = GenreSerializer(data=request.data, instance=genre)
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                response['msg'] = "Genre updated successful."
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                msg = errors[list(errors.keys())[0]][0]
                return Response(data={"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"msg": "Something went wrong. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, genre_id):
        error_message = None
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist as e:
            error_message = "Genre Not Found"
        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)
        genre.delete()

        return Response({"msg": "Genre deleted successful."}, status=status.HTTP_204_NO_CONTENT)


class GenreListView(ListAPIView):
    authentication_classes = (TokenAuthentication, )
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
