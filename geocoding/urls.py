from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + [
    path('admin/', admin.site.urls),
    re_path('', include('location.urls'))
]
