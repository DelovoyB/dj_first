from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from goods.models import Categories

class CategoryViewSetTest(TestCase):
    def setUp(self):        
        """
        Set up a test client and create a category
        """
        self.client = APIClient()

    def test_get_categories(self):        
        """
        Test that a GET to the category list endpoint returns a 200 status
        """
        url = reverse('api:categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        """
        Test that a POST to the category list endpoint with valid data creates a new category
        """        
        url = reverse('api:categories-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(Categories.objects.get().name, 'New Category')

    def test_update_category(self):
        """
        Test that a PUT to the category detail endpoint with valid data updates a category
        """
        category = Categories.objects.create(name='Old Category', slug='old-category')
        url = reverse('api:categories-detail', kwargs={'slug': category.slug})
        data = {'name': 'New Category'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'New Category')

    def test_delete_category(self):
        """
        Test that a DELETE to the category detail endpoint deletes a category

        This test deletes the single category that was created in the setUp method.
        After the deletion, the category count is expected to be zero.
        """
        category = Categories.objects.create(name='Category to delete', slug='category-to-delete')
        url = reverse('api:categories-detail', kwargs={'slug': category.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categories.objects.count(), 0)
