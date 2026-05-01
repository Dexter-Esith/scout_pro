from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/dashboard/')),  # ← ეს დაამატე
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('players.urls')),
    path('reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)