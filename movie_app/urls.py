from . import views
from django.urls import path

app_name = 'movie'
urlpatterns = [
    path("", views.movie_list, name='movie_list'),
    path("movie/error/<str:msg>/", views.movie_error, name='movie_error'),
    path("movie/add", views.movie_add, name='movie_add'),
    path('movie/<int:movie_id>',views.movie_detail,name='movie_details'),
    path('movie/update/<int:movie_id>/', views.movie_update, name='movie_update'),
    path('movie/delete/<int:movie_id>/', views.movie_delete, name='movie_delete'),
    path('movie/review/<int:movie_id>/', views.movie_review, name='movie_review'),
    path('<slug:c_slug>/', views.allMovieCat, name='movieByCat'),
    path('movie/search', views.SearchResult, name='SearchResult'),

]
