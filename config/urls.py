
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Application URLs
    path('', include('core.urls')),

    # PWA service worker served from the website root
    path(
        'service-worker.js',
        serve,
        {
            'path': 'service-worker.js',
            'document_root': settings.BASE_DIR / 'static',
            'show_indexes': False,
        },
    ),
]
