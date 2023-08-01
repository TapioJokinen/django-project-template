from django.urls import path

from myapp.api.views.auth import (
    AuthLoginView,
    AuthLogoutView,
    AuthRefreshView,
    AuthVerifyView,
)

urlpatterns = []

auth_urlpatterns = [
    path("auth/login/", AuthLoginView.as_view(), name="auth_login"),
    path("auth/refresh/", AuthRefreshView.as_view(), name="auth_refresh"),
    path("auth/logout/", AuthLogoutView.as_view(), name="auth_logout"),
    path("auth/verify/", AuthVerifyView.as_view(), name="auth_verify"),
]
