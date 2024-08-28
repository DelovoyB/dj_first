from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase

from users.models import User


class UserModelTest(HypothesisTestCase):

    @given(
        password=st.text(min_size=8, max_size=128, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        last_login=st.datetimes(timezones=st.timezones()),
        is_superuser=st.booleans(),
        username=st.text(min_size=1, max_size=150, alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.+-_")),
        first_name=st.text(min_size=0, max_size=150, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        last_name=st.text(min_size=0, max_size=150, alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
        email=st.emails(),
        is_staff=st.booleans(),
        is_active=st.booleans(),
        date_joined=st.datetimes(timezones=st.timezones()),
        image=st.text(min_size=0, max_size=1000, alphabet=st.characters(blacklist_characters="\x00")),
        phone_number=st.text(min_size=0, max_size=15,  alphabet=st.characters(blacklist_categories=["Cc", "Cs"])),
    )
    def test_create_user(self, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, image, phone_number):
        user = User(password=password, last_login=last_login, is_superuser=is_superuser, username=username, first_name=first_name, last_name=last_name, email=email.lower(), is_staff=is_staff, is_active=is_active, date_joined=date_joined, image=image, phone_number=phone_number)
        user.full_clean()
        user.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.password, password)
        self.assertEqual(user.last_login, last_login)
        self.assertEqual(user.is_superuser, is_superuser)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email.lower())
        self.assertEqual(user.is_staff, is_staff)
        self.assertEqual(user.is_active, is_active)
        self.assertEqual(user.date_joined, date_joined)
        self.assertEqual(user.image, image)
        self.assertEqual(user.phone_number, phone_number)
