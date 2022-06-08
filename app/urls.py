from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='homepage'),
    path('error', views.home, name='error'),
    path('settings', views.settings, name='settings'),
    path('download', views.download, name='download')
]