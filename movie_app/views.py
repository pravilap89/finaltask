from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, MovieRating, Category
from .form import MovieForm


# Create your views here.
def SearchResult(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movie_list=Movie.objects.all().filter(Q(title__contains=query) | Q(description__contains = query))
        return render (request,"search.html",{'query':query,'movies':movie_list})
def movie_list(request):
    movie_all = Movie.objects.all()
    return render(request, "index.html", {'movie_list': movie_all})


def movie_error(request, msg):
    return render(request, 'error.html', {'msg': msg})


def movie_update(request, movie_id):
    if request.user.id is None:
        return redirect('login')

    movie = Movie.objects.get(id=movie_id)
    if movie.user.id != request.user.id:
        return redirect('movie:movie_error', 'This action is not allowed.')

    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('movie:movie_list')
    return render(request, "movie_form.html", {'form': form, 'title': 'Update'})


def movie_delete(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.user.id != request.user.id:
        return redirect('movie:movie_error', 'This action is not allowed.')
    movie.delete()
    return redirect('movie:movie_list')


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, "details.html", {'movie': movie})


def allMovieCat(request, c_slug=None):
    c_page = None
    movie_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movie.objects.all().filter(category=c_page)
    else:
        movie_list = Movie.objects.all()

    paginator = Paginator(movie_list, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        movie = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movie = paginator.page(paginator.num_pages)
    return render(request, "category.html", {'category': c_page, 'movies': movie})


def movie_review(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie_review = MovieRating.objects.filter(user=request.user, movie=movie)
    review = []
    if movie_review.count() > 0:
        review = movie_review[:1].get()

    if request.method == 'POST':
        rating = request.POST.get('stars', 0)
        comments = request.POST.get('comments', 0)
        if movie_review.count() == 0:
            movie_review = MovieRating(user=request.user, movie=movie,
                                       comments=comments, rating=rating)
            movie_review.save()
            return redirect('movie:movie_list')
        else:
            movie_review.update(comments=comments, rating=rating)
            return redirect('movie:movie_review', movie_id)

    m_page = None
    movie_review_all = None
    if movie_id != None:
        movie_review_all = MovieRating.objects.filter(movie=movie)

    paginator = Paginator(movie_review_all, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        all_review = paginator.page(page)
    except (EmptyPage, InvalidPage):
        all_review = paginator.page(paginator.num_pages)

    return render(request, "review.html", {'movie': movie, 'movie_review': review,'all_review':all_review})


def movie_add(request):
    if request.user.id is None:
        return redirect('login')

    form = MovieForm(request.POST or None)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        poster = request.FILES['poster']
        description = request.POST['description']
        actors = request.POST['actors']
        trailer_link = request.POST['trailer_link']
        release = request.POST['release']
        category = Category.objects.get(id=request.POST['category'])
        movie = Movie(title=title, poster=poster, description=description, release=release,
                      actors=actors, trailer_link=trailer_link, category=category, user=request.user)
        movie.save()
        return redirect('movie:movie_list')

    return render(request, "movie_form.html", {'form': form, 'title': 'Add'})
