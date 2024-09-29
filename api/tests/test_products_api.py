from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from goods.models import Categories, Products

class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_products(self):
        url = reverse('api:products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        category = Categories.objects.create(name='Test Category', slug='test-category')
        url = reverse('api:products-list')
        data = {
            'name': 'New Product',
            'price': 10.99,
            'discount': 0.00,
            'quantity': 10,
            'category': category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.get().name, 'New Product')
    
    def test_update_product(self):
        category = Categories.objects.create(name='Test Category', slug='test-category')
        product = Products.objects.create(name='Old Product', slug='old-product', category=category, price=10.99, discount=0.00, quantity=10)
        url = reverse('api:products-detail', kwargs={'slug': product.slug})
        data = {
            'name': 'New Product',
            'price': 12.99,
            'discount': 0.00,
            'quantity': 20,
            'category': category.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, 'New Product')

    def test_delete_product(self):
        category = Categories.objects.create(name='Test Category', slug='test-category')
        product = Products.objects.create(name='Product to delete', slug='product-to-delete', category=category)
        url = reverse('api:products-detail', kwargs={'slug': product.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Products.objects.count(), 0)
