from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase, from_model

from goods.models import Categories, Products


class CategoryModelTest(HypothesisTestCase):

    @given(
        name=st.text(min_size=1, max_size=150,  alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        slug=st.text(min_size=0, max_size=200, alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")),
    )
    def test_create_category(self, name, slug):
        """
        Test that a category can be created with a valid name and slug.

        The ``full_clean`` method is called to ensure that the category is valid
        according to the model's field definitions. The ``save`` method is then
        called to persist the category to the database.

        The test then checks that the category has been created with the expected
        name and slug.
        """
        category = Categories(name=name, slug=slug)
        category.full_clean()
        category.save()

        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, slug)


class ProductModelTest(HypothesisTestCase):

    @given(
        name=st.text(min_size=1, max_size=150,  alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        slug=st.text(min_size=0, max_size=200, alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")),
        description=st.text(min_size=0, max_size=1000, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        image=st.text(min_size=0, max_size=1000, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        price=st.decimals(min_value=0, max_value=10000, places=2),
        discount=st.decimals(min_value=0, max_value=99, places=2),
        quantity=st.integers(min_value=0, max_value=32000),
        category=from_model(Categories)
    )
    def test_create_product(self, name, slug, description, image, price, discount, quantity, category):
        """
        Test that a product can be created with valid name, slug, description, image, price, discount, quantity and category.

        The ``full_clean`` method is called to ensure that the product is valid
        according to the model's field definitions. The ``save`` method is then
        called to persist the product to the database.

        The test then checks that the product has been created with the expected
        name, slug, description, image, price, discount, quantity and category.
        """
        product = Products(name=name, slug=slug, description=description, image=image, price=price, discount=discount, quantity=quantity, category=category)
        product.full_clean()
        product.save()

        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, name)
        self.assertEqual(product.slug, slug)
        self.assertEqual(product.description, description)
        self.assertEqual(product.image, image)
        self.assertEqual(product.price, price)
        self.assertEqual(product.discount, discount)
        self.assertEqual(product.quantity, quantity)
        self.assertEqual(product.category, category)
