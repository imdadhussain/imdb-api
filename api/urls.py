from django.conf.urls import url


from api import views

urlpatterns = [
    url(r'^signup/$', view=views.SignUpView.as_view(), name='sign_up'),
    url(r'^signin/$', view=views.SignInView.as_view(), name='sign_in'),
    url(r'^profile/$', view=views.ProfileView.as_view(), name='profile'),
    url(r'^change_password/$', view=views.ChangePasswordView.as_view(), name='profile'),

]
