from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import get_resolver, reverse
from rest_framework import status
from orders.models import Order
from users.models import User

class OrderViewSetTest(TestCase):
    def setUp(self):
        """
        Set up a test client and create a test user and an order for the user
        
        The test client is set up with the test user authenticated, and the test user
        has a single order with the given details.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(
            user=self.user,
            phone_number='1234567890',
            requires_delivery=True,
            delivery_address='123 Main St',
            payment_on_get=False,
            is_paid=False,
            status='Processing'
        )


    def test_get_orders(self):
        """
        Test that a GET to the order list endpoint returns a 200 status and a list
        of orders for the authenticated user

        The list of orders is expected to contain a single order, with the id of
        the order that was created in the setUp method.
        """
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order.id)


    def test_create_order(self):
        """
        Test that a POST to the order list endpoint with valid data creates a new order
        """
        data = {
            'user': self.user.id,
            'phone_number': '9876543210',
            'requires_delivery': True,
            'delivery_address': 'Test address',
            'payment_on_get': False,
            'is_paid': False,
            'status': 'Processing'
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        last_order = Order.objects.order_by('-created_timestamp').first()
        self.assertEqual(last_order.phone_number, '9876543210')


    def test_update_order(self):
        """
        Test that a PUT to the order detail endpoint with valid data updates an order
        """
        data = {
            'user': self.user.id,
            'phone_number': '1111111111',
            'requires_delivery': False,
            'delivery_address': 'New Address',
            'payment_on_get': True,
            'is_paid': True,
            'status': 'Completed'
        }
        response = self.client.put(f'/api/orders/{self.order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.phone_number, '1111111111')
        self.assertEqual(self.order.status, 'Completed')


    def test_delete_order(self):
        """
        Test that a DELETE to the order detail endpoint deletes an order

        This test deletes the single order that was created in the setUp method.
        After the deletion, the order count is expected to be zero.
        """
        response = self.client.delete(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
