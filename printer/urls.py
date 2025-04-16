from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_request, name='submit_request'),
    path('submit/<str:school_slug>/<int:device_id>/', views.submit_request, name='submit_request'),
    path('success/', views.request_success, name='request_success'),
    path('list/', views.request_list, name='request_list'),
    path('complete/<int:request_id>/', views.mark_completed, name='mark_completed'),

]
