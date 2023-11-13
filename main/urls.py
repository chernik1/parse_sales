from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.form_data, name='form_data'),
    path('delete/', views.delete, name='delete'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('complete/', views.complete, name='complete'),
    path('data_zaku/', views.form_data_zaku, name='form_data_zaku'),
    path('delete_all_zaku/', views.delete_all_zaku, name='delete_all_zaku'),
    path('complete_zaku/', views.complete_zaku, name='complete_zaku'),
    path('complete_all_zaku/', views.complete_all_zaku, name='complete_all_zaku'),
    path('ai_start/', views.ai_start, name='ai_start'),
    path('ai_start_butb/', views.ai_start_butb, name='ai_start_butb'),
]