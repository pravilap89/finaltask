from django.urls import path
from . import views


urlpatterns = [
    path('registration', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('update/<int:pk>/', views.ProfileUpdateView.as_view(), name='updateview'),
    path('update', views.update, name='update'),
]
