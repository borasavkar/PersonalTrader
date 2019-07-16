
from django.urls import path,include
from . import views

app_name='ticker'

urlpatterns = [
    path('index.html', views.index, name='index'),
    path('', views.index, name='home'),
   
]