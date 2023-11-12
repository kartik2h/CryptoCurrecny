from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import CreateUserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .forms import CreateUserForm, UserProfileForm


def home_view(request):
    about = About.objects.first()
    services = Service.objects.all()
    works = RecentWork.objects.all()

    context = {
        'about': about,
        'services': services,
        'works': works,
    }

    return render(request, 'core/home.html', context)


def registerPage(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = user.username
            messages.success(request, 'Account created for ' + username)
            return redirect('login')

    else:
        user_form = CreateUserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'core/login.html')
    context = {}
    return render(request, 'core/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


@login_required
def index(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        profile_pic = user_profile.profile_pic
    except UserProfile.DoesNotExist:
        profile_pic = None

    return render(request, 'core/home1.html', {'profile_pic': profile_pic})
