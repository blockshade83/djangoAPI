from django.urls import include, path
from . import views
from . import api
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('status_update/', views.status_update, name = 'status_update'),
    path('search/', views.search, name = 'search'),
    path('get_profile/<int:user_id>', views.get_profile, name = 'get_profile'),
    path('connect', views.connect_initiate, name = 'connect'),
    path('connect_accept', views.connect_accept, name = 'connect_accept'),
    path('connect_reject', views.connect_reject, name = 'connect_reject'),
    path('connect_withdraw', views.connect_withdraw, name = 'connect_withdraw'),
    path('current_contacts', views.current_contacts, name = 'current_contacts'),
    path('incoming_connection_requests', views.incoming_connection_requests, name = 'incoming_connection_requests'),
    path('outgoing_connection_requests', views.outgoing_connection_requests, name = 'outgoing_connection_requests'),
    path('update_profile', views.update_profile, name = 'update_profile'),
    path('upload_photo', views.upload_photo, name = 'upload_photo'),
    path('gallery', views.gallery, name = 'gallery'),
    path('get_gallery/<int:user_id>', views.get_gallery, name = 'get_gallery'),
    path('api/users/', api.get_users, name = 'all_users'),
    path('api/user_posts/<str:username>', api.get_user_posts, name = 'get_user_posts'),
    path('api/user_contacts/<str:username>', api.get_user_contacts, name = 'get_user_contacts'),
    path('api/pending_connection_requests/', api.pending_connection_requests, name = 'pending_connection_requests')
]
