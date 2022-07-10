from django.urls import include, path
from . import views
# from . import api
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register')
]
