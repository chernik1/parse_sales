from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.form_data, name='form_data'),
    path('delete/', views.delete, name='delete'),
]