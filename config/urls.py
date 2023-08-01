from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from myapp.api.urls import auth_urlpatterns

urlpatterns = [
    *auth_urlpatterns,
    path("api/", include("myapp.api.urls")),
]

if settings.DEBUG:
    dev_urlpatterns = [
        path("admin/", admin.site.urls),
    ]

    urlpatterns += dev_urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
