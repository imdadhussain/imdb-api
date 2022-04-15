from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView, ListAPIView

from api.permissions import IsAdmin
from api.models import Movie, Director
from api.Serializers import MovieSerializer


class MoviesList(ListAPIView):
    """
    List searching movies.
    """
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-created_at')
        return queryset

    def paginate_queryset(self, queryset):
        page = self.request.query_params.get('page')
        size = self.request.query_params.get('size')
        if not size:
            size = 20
        if not page:
            page = 1
        size = int(size)
        page = int(page)

        end = size * page
        start = end - size
        queryset = queryset[start: end]
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        director = request.query_params.get('director')
        if director:
            queryset = queryset.filter(director__name__icontains=director)

        genre = request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        imdb_score = request.query_params.get('imdb_score')
        if imdb_score:
            queryset = queryset.filter(imdb_score=imdb_score)

        popularity = request.query_params.get('popularity')
        if popularity:
            queryset = queryset.filter(popularity=popularity)

        queryset = self.paginate_queryset(queryset)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data={"movie": serializer.data}, status=status.HTTP_200_OK)


class MovieView(GenericAPIView):
    """Handle creating, updating and deleting movies"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = MovieSerializer
    permission_classes = (IsAdmin, IsAuthenticated, )

    def post(self, request):
        data = request.data
        if Movie.objects.filter(name=data['name']).exists():
            return Response(data={"msg": "Movie with same already present."}, status=status.HTTP_409_CONFLICT)

        try:
            movie = Movie.objects.create(
                name=data['name'],
                imdb_score=data['imdb_score'],
                popularity=data['popularity'],
                director_id=data['director_id']
            )
            for genre_id in data['genre']:
                movie.genre.add(genre_id)
            movie.save()
            serializer = MovieSerializer(instance=movie)
            response = serializer.data
            response['msg'] = "Movie created successful."
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"msg": "Invalid Request."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, movie_id):
        data = request.data
        error_message = None
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist as e:
            error_message = "Movie Not Found"
        if Movie.objects.filter(name=data['name']).exclude(id=movie_id).exists():
            return Response(data={"msg": "Movie with same already present."}, status=status.HTTP_409_CONFLICT)
        try:
            director = Director.objects.get(id=data['director_id'])
        except Director.DoesNotExist as e:
            error_message = "Director Not Found"

        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)

        try:
            movie.name = data['name']
            movie.imdb_score = data['imdb_score']
            movie.popularity = data['popularity']
            movie.director = director
            movie.genre.clear()
            for genre_id in data['genre']:
                movie.genre.add(genre_id)
            movie.save()
            serializer = MovieSerializer(instance=movie)
            response = serializer.data
            response['msg'] = "Movie created successful."
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"msg": "Invalid Request."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        error_message = None
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist as e:
            error_message = "Movie Not Found"
        if error_message:
            return Response(data={"msg": error_message}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response({"msg": "Movie deleted successful."}, status=status.HTTP_204_NO_CONTENT)
