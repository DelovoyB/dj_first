from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase, from_model

from carts.models import Cart
from goods.models import Products, Categories
from users.models import User


class CartModelTest(HypothesisTestCase):

    @given(
        user=from_model(User),
        product=from_model(Products, category=from_model(Categories)),
        quantity=st.integers(min_value=0, max_value=32766),
        session_key=st.text(min_size=0, max_size=32, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        created_timestamp=st.datetimes(timezones=st.timezones()),
    )
    def test_create_cart(self, user, product, quantity, session_key, created_timestamp):
        cart = Cart(user=user, product=product, quantity=quantity, session_key=session_key, created_timestamp=created_timestamp)
        cart.full_clean()
        cart.save()

        self.assertIsNotNone(cart.id)
        self.assertEqual(cart.user, user)
        self.assertEqual(cart.product, product)
        self.assertEqual(cart.quantity, quantity)
        self.assertEqual(cart.session_key, session_key)
        self.assertIsNotNone(cart.created_timestamp)
