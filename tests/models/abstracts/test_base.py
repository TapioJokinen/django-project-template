from django.db.models import Count
from django.test import TestCase
from myapp.models.user import User

from tests.factories import UserFactory


class BaseModelTests(TestCase):
    def test_to_dict(self):
        user = UserFactory()
        user_dict = user.to_dict()

        self.assertEqual(
            user_dict,
            {
                "id": user.id,
                "date_added": user.date_added,
                "date_updated": user.date_updated,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "last_active": user.last_active,
                "groups": [],
                "user_permissions": [],
            },
        )

        user_dict = user.to_dict(
            exclude=[
                "id",
                "password",
                "last_login",
                "is_superuser",
                "date_added",
                "date_updated",
                "first_name",
                "last_name",
                "is_staff",
                "is_active",
                "last_active",
                "groups",
                "user_permissions",
            ]
        )

        self.assertEqual(user_dict, {"email": user.email})

        user = User.objects.annotate(groups_count=Count("groups")).get(id=user.id)

        user_dict = user.to_dict(
            exclude=[
                "id",
                "password",
                "last_login",
                "is_superuser",
                "date_added",
                "date_updated",
                "first_name",
                "last_name",
                "is_staff",
                "is_active",
                "last_active",
                "groups",
                "user_permissions",
            ],
            include=["groups_count"],
        )

        self.assertEqual(user_dict, {"email": user.email, "groups_count": 0})
