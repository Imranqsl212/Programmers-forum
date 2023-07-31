from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create/', views.createRoom, name='create'),
    path('update/<str:pk>/', views.updateRoom, name='update'),
    path('delete/<str:pk>/', views.deleteRoom, name='delete'),
    path('log_in/', views.loginPage, name='Log_in'),
    path('log_out/', views.logoutPage, name='Log_out'),
    path('reg/', views.registerPage, name='reg'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('edit-user', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activities/', views.activities, name='activities')
]
