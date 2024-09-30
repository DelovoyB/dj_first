from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase, from_model

from goods.models import Products, Categories
from orders.models import Order, OrderItem
from users.models import User


class OrderModelTest(HypothesisTestCase):

    @given(
        user=from_model(User),
        created_timestamp=st.datetimes(timezones=st.timezones()),
        phone_number=st.text(min_size=1, max_size=20,  alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        requires_delivery=st.booleans(),
        delivery_address=st.text(min_size=0, max_size=1000, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        payment_on_get=st.booleans(),
        is_paid=st.booleans(),
        status=st.text(min_size=1, max_size=20, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
    )
    def test_create_order(self, user, created_timestamp, phone_number, requires_delivery, delivery_address, payment_on_get, is_paid, status):
        """
        Test that an order can be created with valid user, created timestamp, phone number, requires delivery, delivery address, payment on get, is paid and status.

        The ``full_clean`` method is called to ensure that the order is valid
        according to the model's field definitions. The ``save`` method is then
        called to persist the order to the database.

        The test then checks that the order has been created with the expected
        user, created timestamp, phone number, requires delivery, delivery address,
        payment on get, is paid and status.
        """
        order = Order(
            user=user,
            created_timestamp=created_timestamp,
            phone_number=phone_number,
            requires_delivery=requires_delivery,
            delivery_address=delivery_address,
            payment_on_get=payment_on_get,
            is_paid=is_paid,
            status=status
        )
        order.full_clean()
        order.save()

        self.assertIsNotNone(order.id)
        self.assertEqual(order.user, user)
        self.assertIsNotNone(order.created_timestamp)
        self.assertEqual(order.phone_number, phone_number)
        self.assertEqual(order.requires_delivery, requires_delivery)
        self.assertEqual(order.delivery_address, delivery_address)
        self.assertEqual(order.payment_on_get, payment_on_get)
        self.assertEqual(order.is_paid, is_paid)
        self.assertEqual(order.status, status)


class OrderItemModelTest(HypothesisTestCase):

    @given(
        order=from_model(Order, user=from_model(User)),
        product=from_model(Products, category=from_model(Categories)),
        name=st.text(min_size=1, max_size=150, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        price=st.decimals(min_value=0, max_value=10000, places=2),
        quantity=st.integers(min_value=0, max_value=32000),
        created_timestamp=st.datetimes(timezones=st.timezones()),
    )
    def test_create_order_item(self, order, product, name, price, quantity, created_timestamp):
        """
        Test that an order item can be created with valid order, product, name, price, quantity and created timestamp.

        The ``full_clean`` method is called to ensure that the order item is valid
        according to the model's field definitions. The ``save`` method is then
        called to persist the order item to the database.

        The test then checks that the order item has been created with the expected
        order, product, name, price, quantity and created timestamp.
        """
        order_item = OrderItem(
            order=order,
            product=product,
            name=name,
            price=price,
            quantity=quantity,
            created_timestamp=created_timestamp
        )
        order_item.full_clean()
        order_item.save()

        self.assertIsNotNone(order_item.id)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, product)
        self.assertEqual(order_item.name, name)
        self.assertEqual(order_item.price, price)
        self.assertEqual(order_item.quantity, quantity)
        self.assertIsNotNone(order_item.created_timestamp)
