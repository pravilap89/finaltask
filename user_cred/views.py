from urllib import request

from django.contrib import messages, auth
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from .form import profileForm


# Create your views here.
class ProfileUpdateView(UpdateView):
    template_name = 'update.html'
    fields = ('username', 'first_name', 'last_name', 'email')
    context_object_name = 'request.user'
    model = User

    def get_success_url(self):
        return reverse_lazy('movie:movie_list')


def update(request):
    if request.method == 'POST':
        form = profileForm(data=request.POST, instance=request.user)
        username_exists = User.objects.all().filter(Q(username=form.data['username']) & ~Q(id=request.user.id))
        print(username_exists)
        if username_exists.exists():
            messages.info(request, "Username taken")
            return redirect('update')
        else:
            email_exists = User.objects.all().filter(Q(email=form.data['email']) & ~Q(id=request.user.id))
            if email_exists.exists():
                messages.info(request, "Email Id exists")
                return redirect('update')
        update = form.save(commit=False)
        update.user = request.user
        update.save()
    else:
        form = profileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Id exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Password missmatch")
            return redirect('register')
    return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')
