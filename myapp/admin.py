from django.contrib import admin

from myapp.forms import UserChangeForm, UserCreationForm
from myapp.models import User


class UserAdmin(admin.ModelAdmin):
    model = User

    add_form = UserCreationForm

    form = UserChangeForm

    search_fields = (
        "id",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("email",)

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = (
        (
            "User details",
            {"fields": ("email", "first_name", "last_name")},
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
