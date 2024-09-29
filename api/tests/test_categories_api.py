from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from goods.models import Categories

class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_categories(self):
        url = reverse('api:categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse('api:categories-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(Categories.objects.get().name, 'New Category')

    def test_update_category(self):
        category = Categories.objects.create(name='Old Category', slug='old-category')
        url = reverse('api:categories-detail', kwargs={'slug': category.slug})
        data = {'name': 'New Category'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'New Category')

    def test_delete_category(self):
        category = Categories.objects.create(name='Category to delete', slug='category-to-delete')
        url = reverse('api:categories-detail', kwargs={'slug': category.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categories.objects.count(), 0)
