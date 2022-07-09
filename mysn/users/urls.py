from django.urls import include, path
from . import views
# from . import api

urlpatterns = [
    path('', views.index, name='index')
]
