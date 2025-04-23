from django.urls import path
from . import views
from printer.views import ASRequestListView
urlpatterns = [
    path('', views.submit_request, name='submit_request'),
    path('submit/<str:school_slug>/<int:device_id>/', views.submit_request, name='submit_request'),
    path('success/', views.request_success, name='request_success'),
    path('list/', ASRequestListView.as_view(), name='request_list'),
    path('complete/<int:request_id>/', views.mark_completed, name='mark_completed'),
    path('api/latest/', views.latest_request_time, name='latest_request_time'),
    path('export/excel/', views.export_as_excel, name='export_as_excel'),
    path('comment/<int:request_id>/', views.save_comment, name='save_comment'),


]
