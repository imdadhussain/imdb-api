from django.contrib import admin

from api.models import User, Director, Genre, Movie


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']


class DirectorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class MovieAdmin(admin.ModelAdmin):
    search_fields = ['name', 'director__name', 'genre__name']
    list_filter = ('director', 'genre')


admin.site.register(User, UserAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
