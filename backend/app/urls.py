from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='homepage'),
    path('submit-link', views.submit, name='submit'),
    path('download', views.download, name='download')
]