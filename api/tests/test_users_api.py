from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

User = get_user_model()

class UserViewSetTest(TestCase):
    def setUp(self):
        """
        Set up a test user and an admin user, and log in as the test user
        """        
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')
        self.client.force_login(self.user)

    def test_list_users_authenticated(self):       
        """
        Test that a user can list all users if they are authenticated
        """
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_list_users_unauthenticated(self):
        """
        Test that a user can not list all users if they are not authenticated
        """
        self.client.logout()
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_authenticated(self):
        """
        Test that an admin user can retrieve the details of any user if they are authenticated
        """
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_user_unauthenticated(self):
        """
        Test that a user can not retrieve the details of any user if they are not authenticated
        """
        self.client.logout()
        response = self.client.get(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_admin_only(self):
        """
        Test that only an admin user can create a new user
        """
        self.client.logout()
        self.client.force_login(self.admin_user)

        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('api:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_non_admin(self):
        """
        Test that a non admin user can not create a new user
        """        
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('api:user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_admin_only(self):        
        """
        Test that only an admin user can update a user
        """        
        self.client.logout()
        self.client.force_login(self.admin_user)

        data = {
            'username': 'updateduser'
        }
        response = self.client.put(reverse('api:user-detail', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_update_user_non_admin(self):        
        """
        Test that a non admin user can not update a user
        """       
        data = {
            'username': 'updateduser'
        }
        response = self.client.put(reverse('api:user-detail', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_admin_only(self):
        """
        Test that only an admin user can delete a user
        """       
        self.client.logout()
        self.client.force_login(self.admin_user)

        response = self.client.delete(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_non_admin(self):        
        """
        Test that a non admin user can not delete a user
        """        
        response = self.client.delete(reverse('api:user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
