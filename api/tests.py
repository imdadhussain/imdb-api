import json
from io import StringIO
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse

from api.Serializers import SignUpSerializer


class SignUpTestCase(APITestCase):

    def test_user_cannot_register_with_in_complete_data(self):
        data = {
            "name": "testinvalid",
            "password": "admin123",
            "confirm_password": "admin123",
        }
        response = self.client.post(reverse('sign_up'), data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        data = {
            "email": "test@mailinator.com",
            "name": "Test",
            "password": "admin123",
            "confirm_password": "admin123",
            "dob": "07-01-1992"
        }
        response = self.client.post(reverse('sign_up'), data)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['is_admin'], False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_register(self):
        data = {
            "name": "testcase",
            "dob": "07-11-1992",
            "email": "testcase@mailinator.com",
            "password": "admin123",
            "confirm_password": "admin123",
            "is_admin": True
        }
        response = self.client.post(reverse('sign_up'), data)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['is_admin'], True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SignInTestCase(APITestCase):

    def setUp(self):
        data = {
            "email": "testcase@mailinator.com",
            "name": "TestCase",
            "password": "admin123",
            "confirm_password": "admin123",
            "dob": "07-01-1992"
        }
        serializer = SignUpSerializer(data=data)
        serializer.is_valid()
        user_instance = serializer.save()
        # generate token
        token_instance = Token.objects.create(user=user_instance)
        token_instance.generate_key()
        token_instance.save()

    def test_invalid_login(self):
        data = {
            "email": "testcase@mailinator.com",
            "password": "admin@123"
        }
        response = self.client.post(reverse('sign_in'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login(self):
        data = {
            "email": "testcase@mailinator.com",
            "password": "admin123"
        }
        response = self.client.post(reverse('sign_in'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChangePasswordTestCase(APITestCase):

    def setUp(self):
        data = {
            "email": "testcase@mailinator.com",
            "name": "TestCase",
            "password": "admin123",
            "confirm_password": "admin123",
            "dob": "07-01-1992"
        }
        serializer = SignUpSerializer(data=data)
        serializer.is_valid()
        user_instance = serializer.save()
        # generate token
        token_instance = Token.objects.create(user=user_instance)
        token_instance.generate_key()
        token_instance.save()

        self.token = Token.objects.get(user=user_instance)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_invalid_change_password(self):
        data = {
            "email": "testcase@mailinator.com",
            "password": "admin@123",
            "password2": "admin@123",
            "old_password": "pass@123"

        }
        response = self.client.post(reverse('change_password'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        data = {
            "email": "testcase@mailinator.com",
            "password": "admin@123",
            "password2": "admin@123",
            "old_password": "admin123"

        }
        response = self.client.post(reverse('change_password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieTestCase(APITestCase):
    """
    Unit test case for custom management command to populate database and search api.
    """

    def test_command_output(self):
        out = StringIO()
        call_command('populate_movie_data', stdout=out)
        self.assertIn('Successfully populated the database', out.getvalue().strip())

    def test_search_movies(self):
        params = {'name': 'Ghost'}
        response = self.client.get(reverse('movie_search'), params)
        json_response = response.json()['movie']
        assert response.status_code == status.HTTP_200_OK

    def test_search_movies_with_pagination(self):
        params = {'name': 'Wizard', 'size': 10, 'page': 1}
        response = self.client.get(reverse('movie_search'), params)
        json_response = response.json()['movie']
        assert response.status_code == status.HTTP_200_OK

    def test_search_movies_by_genre(self):
        params = {'genre': 'War'}
        response = self.client.get(reverse('movie_search'), params)
        json_response = response.json()['movie']
        assert response.status_code == status.HTTP_200_OK

    def test_search_movies_by_director(self):
        params = {'director': 'Algar'}
        response = self.client.get(reverse('movie_search'), params)
        json_response = response.json()['movie']
        assert response.status_code == status.HTTP_200_OK
