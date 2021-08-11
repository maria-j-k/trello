from django.contrib import admin
from django.urls import include, path
from users.views import api_root

urlpatterns = [
    path('', api_root, name='root'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
]
