from django.urls import include, path
# from django.contrib.auth import views as auth_views
from . import views
# from . import api
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    # path('login/', auth_views.LoginView.as_view(), name = 'login'),
    # path('logout/', auth_views.LogoutView.as_view(), name = 'logout')
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('status_update/', views.status_update, name = 'status_update')
]
