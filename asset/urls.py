from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from django.urls import path, include
from django.urls import get_resolver
from catalog.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Main application
    path('catalog/', include('catalog.urls', namespace='catalog')),
    
    # Redirect root to catalog
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
    
    # API endpoints
    path('api/', include('catalog.urls', namespace='catalog-api')),  # Ensure a unique namespace

    path('accounts/', include('django.contrib.auth.urls')), 
    path('', CustomLoginView.as_view(), name='login'),  # Default view

    path('auth/', include('social_django.urls', namespace='social')),  # Social auth URLs





]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def show_urls(urllist, depth=0):
    for entry in urllist:
        print("  " * depth, entry)
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

show_urls(get_resolver().url_patterns)