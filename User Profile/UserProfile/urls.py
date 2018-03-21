from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^', include('user_profile.urls')),
    url('^', include('django.contrib.auth.urls')),

]
