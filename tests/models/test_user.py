from django.contrib.auth import get_user_model
from django.test import TestCase
from myapp.models.user import User

from tests.factories import UserFactory


class UserManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.User = get_user_model()

    def test_create_user(self) -> None:
        user = self.User.objects.create_user(email="foo@bar.com", password="foobar", first_name="foo", last_name="bar")
        self.assertEqual(user.email, "foo@bar.com")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "bar")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaisesMessage(ValueError, "Email is required."):
            self.User.objects.create_user(email=None, password="foobar", first_name="foo", last_name="bar")

        with self.assertRaisesMessage(ValueError, "First name is required."):
            self.User.objects.create_user(email="foo@bar.com", password="foobar", last_name="bar")

        with self.assertRaisesMessage(ValueError, "Last name is required."):
            self.User.objects.create_user(email="foo@bar.com", password="foobar", first_name="foo")

    def test_create_superuser(self) -> None:
        user = self.User.objects.create_superuser(
            email="foo@bar.com", password="foobar", first_name="foo", last_name="bar"
        )
        self.assertEqual(user.email, "foo@bar.com")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "bar")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        with self.assertRaisesMessage(ValueError, "Email is required."):
            self.User.objects.create_superuser(email=None, password="foobar", first_name="foo", last_name="bar")

        with self.assertRaisesMessage(ValueError, "First name is required."):
            self.User.objects.create_superuser(email="foo@bar.com", password="foobar", last_name="bar")

        with self.assertRaisesMessage(ValueError, "Last name is required."):
            self.User.objects.create_superuser(email="foo@bar.com", password="foobar", first_name="foo")

        with self.assertRaisesMessage(ValueError, "Superuser must be staff."):
            self.User.objects.create_superuser(
                email="foo@bar.com",
                password="foobar",
                first_name="foo",
                last_name="bar",
                is_staff=False,
            )

        with self.assertRaisesMessage(ValueError, "Superuser must be superuser"):
            self.User.objects.create_superuser(
                email="foo@bar.com",
                password="foobar",
                first_name="foo",
                last_name="bar",
                is_superuser=False,
            )


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.User = get_user_model()

    def test_user_model(self) -> None:
        self.assertTrue(self.User == User)

    def test_username_field(self) -> None:
        self.assertEqual(self.User.USERNAME_FIELD, "email")

    def test_required_fields(self) -> None:
        self.assertEqual(self.User.REQUIRED_FIELDS, ["first_name", "last_name"])

    def test_string_representation(self) -> None:
        user = self.User.objects.create_user(email="foo@bar.com", password="foobar", first_name="foo", last_name="bar")

        self.assertEqual(str(user), "foo@bar.com")

    def test_user_to_dict(self):
        user = UserFactory()

        correct_keys = [
            "id",
            "date_added",
            "date_updated",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "last_active",
            "groups",
            "user_permissions",
        ]

        for k in user.to_dict().keys():
            self.assertIn(k, correct_keys)
            correct_keys.remove(k)

        self.assertTrue(len(correct_keys) == 0)

    def test_user_to_dict_with_exclude(self):
        user = UserFactory()

        correct_keys = [
            "id",
            "date_added",
            "date_updated",
            "email",
            "is_active",
            "last_active",
            "groups",
            "user_permissions",
        ]

        for k in user.to_dict(exclude=["first_name", "last_name"]).keys():
            self.assertIn(k, correct_keys)
            correct_keys.remove(k)

        self.assertTrue(len(correct_keys) == 0)
