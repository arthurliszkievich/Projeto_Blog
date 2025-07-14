
from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='home'),
    path('kitchen-sink/', views.kitchen_sink, name='kitchen-sink'),
    path('page/', views.page, name='page'),
    path('post/', views.post, name='post'),
]
