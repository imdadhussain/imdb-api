from django.contrib.auth.hashers import check_password


def password_auth(user, password):
    return check_password(password, user.password)
