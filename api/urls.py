from django.conf.urls import url


from api import views

urlpatterns = [
    url(r'^signup/$', view=views.SignUpView.as_view(), name='sign_up'),
    url(r'^signin/$', view=views.SignInView.as_view(), name='sign_in'),
    url(r'^profile/$', view=views.ProfileView.as_view(), name='profile'),
    url(r'^change_password/$', view=views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^directors/$', views.DirectorView.as_view(), name='create_director'),
    url(r'^directors/(?P<director_id>[0-9]+)/$', views.DirectorView.as_view(), name='update_delete_director'),
    url(r'^directors/all/$', views.DirectorListView.as_view(), name='all_directors'),
    url(r'^genres/$', views.GenreView.as_view(), name='create_genre'),
    url(r'^genres/(?P<genre_id>[0-9]+)/$', views.GenreView.as_view(), name='update_delete_genre'),
    url(r'^genres/all/$', views.GenreListView.as_view(), name='all_genres'),
    url(r'^movies/$', view=views.MoviesList.as_view(), name='movie_search'),
    url(r'^movie/$', view=views.MovieView.as_view(), name='create_movie'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.MovieView.as_view(), name='update_delete_director'),

]
