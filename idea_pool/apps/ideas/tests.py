import factory
import json

from django.test import TestCase
from django.urls import reverse

from accounts.factories import User
from .factories import IdeaFactory


class IdeaTestCase(TestCase):
    def setUp(self):
        IdeaFactory()
        IdeaFactory()
        IdeaFactory()
        IdeaFactory()

    def test_create_idea(self):
        user = User.objects.create_user(email='test1@example.com',
                                        username='TestUser',
                                        password='password')
        url = reverse('access-tokens')
        idea_url = reverse('ideas-dash')
        idea = {
            'content': 'Some great idea',
            'confidence': 7,
            'impact': 7,
            'ease': 7
        }
        tokens = self.client.post(url,
                                  json.dumps({'email': user.email, 'password':user.password}),
                                  content_type='application/json')
        jwt_auth = tokens.data['jwt']
        headers = {'HTTP_AUTHORIZATION': jwt_auth}
        response = self.client.post(idea_url, json.dumps(idea),
                                    content_type='application/json',
                                    follow=True,
                                    **headers)
        self.assertEqual(response.status_code, 201)

    def test_create_idea_fail(self):
        """Request should fail if Idea ease, confidence or impact are not between 1 and 10."""
        user = User.objects.create_user(email='test1@example.com',
                                        username='TestUser',
                                        password='password')
        url = reverse('access-tokens')
        idea_url = reverse('ideas-dash')
        idea = {
            'content': 'Some great idea',
            'confidence': 0,
            'impact': 11,
            'ease': 7
        }
        tokens = self.client.post(url,
                                  json.dumps({'email': user.email, 'password':user.password}),
                                  content_type='application/json')
        jwt_auth = tokens.data['jwt']
        headers = {'HTTP_AUTHORIZATION': jwt_auth}
        response = self.client.post(idea_url, json.dumps(idea),
                                    content_type='application/json',
                                    follow=True,
                                    **headers)
        self.assertEqual(response.status_code, 400)

    def test_list_ideas(self):
        user = User.objects.create_user(email='test100@example.com',
                                        username='TestUser',
                                        password='password')
        url = reverse('access-tokens')
        idea_url = reverse('ideas-dash')

        tokens = self.client.post(url,
                                  json.dumps({'email': user.email,
                                              'password': user.password}),
                                  content_type='application/json')
        jwt_auth = tokens.data['jwt']
        headers = {'HTTP_AUTHORIZATION': jwt_auth}
        response = self.client.get(idea_url,
                                    content_type='application/json',
                                    **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
