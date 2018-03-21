from django.conf.urls import url

from . import views

app_name = 'user_profile'

urlpatterns = [
     url(r'^login_user/$',views.login_user,name='login_user'),
     url(r'^logout/$', views.logout, name='logout'),
     url(r'^signup/$',views.signup,name='signup'),
     url(r'^client/$',views.client,name='client'),
     url(r'^profile/$',views.profile,name='profile'),
     url(r'^account_activation_sent/$',views.account_activation_sent, name='account_activation_sent'),
     url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),

     # /package/

 ]
