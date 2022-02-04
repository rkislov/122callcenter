from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('calls.urls', namespace='calls')),
    path('users/', include('django.contrib.auth.urls')),
    path('video/', include('video.urls', namespace='video')),
    path('admin/', admin.site.urls),
]
