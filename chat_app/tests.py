from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status

class ModeratorTests(APITestCase):
    def setUp(self):
        self.moderator = User.objects.create_user(username='mod', password='modpass')
        self.user = User.objects.create_user(username='user', password='userpass')
        self.group = Group.objects.create(name='Модератор')
        self.moderator.groups.add(self.group)
        self.client.login(username='mod', password='modpass')

    def test_block_user(self):
        response = self.client.post(f'/api/users/{self.user.id}/block/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
