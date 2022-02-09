from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('calls.urls', namespace='calls')),
    path('users/', include('django.contrib.auth.urls')),
    path('video/', include('video.urls', namespace='video')),
    path('hospital/', include('hospitals.urls', namespace='hospitals')),
    path('supervisers/', include('supervisers.urls', namespace='supervisers')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('doctor/', include('doctors.urls', namespace='doctors')),
    path('admin/', admin.site.urls),
]
