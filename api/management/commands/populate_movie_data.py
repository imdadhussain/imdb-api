import json

from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import Movie, Genre, Director


class Command(BaseCommand):
    """
    populate movies data from provided imdb.json dump
    """

    def handle(self, *args, **options):
        filepath = f"{settings.BASE_DIR}/imdb.json"
        total_movies = 0
        total_movie_created = 0
        total_genre_created = 0
        with open(filepath, 'r') as f:
            raw_data = f.read()
            data = json.loads(raw_data)
            for movie_item in data:
                total_movies += 1
                director, director_created = Director.objects.get_or_create(name=movie_item.get('director'))
                if Movie.objects.filter(name=movie_item.get('name')).filter().exists():
                    movie.popularity = movie_item.get('99popularity')
                    movie.director = director
                    movie.imdb_score = movie_item.get('imdb_score')

                else:
                    movie = Movie.objects.create(
                        name=movie_item.get('name'),
                        imdb_score=movie_item.get('imdb_score'),
                        popularity=movie_item.get('99popularity'),
                        director=director
                    )
                    total_movie_created += 1
                genre_list = movie_item.get('genre')
                # create genre for each genre in list and attach to current movie
                for name in genre_list:
                    name = name.strip()
                    genre, genre_created = Genre.objects.get_or_create(name=name)
                    movie.genre.add(genre)
                    if genre_created:
                        total_genre_created += 1
                movie.save()
        f.close()
        print(f"Total Movies - {total_movies} \n"
              f"Total Movies Created - {total_movie_created}\n"
              f"Total Genre Created - {total_genre_created}\n"
              )
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
