from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name='index'),
    path('add/',views.add),
    path('delete/<int:todo_id>/',views.delete),
    path('login/',views.login,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('register/', views.register, name='register'),
    path('profile/',views.profile,name='profile'),
]