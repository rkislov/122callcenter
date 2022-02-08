from django.urls import path

from . import views


app_name = "profiles"


urlpatterns = [
    path('lk/', views.show, name='lk'),
    path('signup/', views.signup, name='signup'),
    path('lk/edit/', views.edit, name='lk-edit'),
    # path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),

]
