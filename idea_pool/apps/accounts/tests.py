import json
import jwt

from django.test import TestCase
from django.urls import reverse

from .factories import UserFactory, User


class UserAuthTestCase(TestCase):
    def test_user_signup(self):
        url = reverse('users-create')
        user = {
            'username': 'FakeUser',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
            'email': 'faker@example.com'
        }

        response = self.client.post(url, json.dumps(user),
                                    content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        url = reverse('access-tokens')
        user = User.objects.create_user(email='test1@example.com',
                                        username='TestUser',
                                        password='password')
        login_data = {'email': user.email, 'password': user.password}

        response = self.client.post(url, json.dumps(login_data),
                                    content_type='application/json')

        refresh_token = response.data['refresh_token']
        jwt_token = response.data['jwt']
        # Test both tokens are in response
        self.assertTrue('jwt' in response.data)
        self.assertTrue('refresh_token' in response.data)

        # Test JWT decode success
        payload = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
        self.assertEqual(payload.get('email'), user.email)

        # Test JWT refresh success
        refresh_url = reverse('refresh-tokens')
        refresh_response = self.client.post(refresh_url,
                                            json.dumps({'refresh_token': refresh_token}),
                                            content_type='application/json')
        self.assertTrue('jwt' in refresh_response.data)

    def test_user_logout(self):
        url = reverse('access-tokens')
        user = User.objects.create_user(email='test34@example.com',
                                        username='Test34User',
                                        password='password')
        login_data = {'email': user.email, 'password': user.password}

        response = self.client.post(url, json.dumps(login_data),
                                    content_type='application/json')
        refresh_token = {'refresh_token': response.data['refresh_token']}

        logout_url = reverse('access-tokens')
        response = self.client.delete(logout_url, json.dumps(refresh_token),
                                      content_type='application/json')

        self.assertEqual(response.status_code, 204)

