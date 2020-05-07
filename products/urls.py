from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('home.urls')),
    path('', views.index, name='index'),
    path('test', views.index, name='index'),
]