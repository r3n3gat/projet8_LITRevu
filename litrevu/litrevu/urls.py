# litrevu/urls.py

from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
]
