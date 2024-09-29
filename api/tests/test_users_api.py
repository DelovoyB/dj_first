from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

User = get_user_model()

class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_list_users_authenticated(self):
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_list_users_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_authenticated(self):
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_user_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_admin_only(self):
        self.client.logout()
        self.client.login(username='adminuser', password='adminpassword')

        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('api:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_non_admin(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('api:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_admin_only(self):
        self.client.logout()
        self.client.login(username='adminuser', password='adminpassword')

        data = {
            'username': 'updateduser'
        }
        response = self.client.put(reverse('api:user-detail', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_update_user_non_admin(self):
        data = {
            'username': 'updateduser'
        }
        response = self.client.put(reverse('api:user-detail', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_admin_only(self):
        self.client.logout()
        self.client.login(username='adminuser', password='adminpassword')

        response = self.client.delete(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_non_admin(self):
        response = self.client.delete(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
