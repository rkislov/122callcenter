from django.urls import path

from . import views

app_name="supervisers"

urlpatterns = [
    path('', views.SuperviserShowCall.as_view(), name='main'),
    path('call/<int:pk>', views.SuperviserShow.as_view(), name='show'),
    path('call/edit/<int:pk>', views.SuperviserEdit.as_view(), name='edit'),
    path('update/', views.update, name='update'),
]
