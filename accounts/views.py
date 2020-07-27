from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm
from django.views import View
from .models import Profile
from django.utils import timezone
from django.views.generic import UpdateView, DetailView
from .backends import EmailBackend
from .forms import UpdateForm
from django.contrib.auth.views import LogoutView


class SignUp(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        context = {
            'form': form,
            'title': "Регистрация"
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            form.send_email(request, request.POST['email'])
            user = form.save() 
            auth_login(request, user)
            return redirect('home')
        else:
            error = form.errors.as_json()
            form = SignUpForm()
            context = {
                'form': form,
                'error': error,
                'title': "Регистрация"
            }
            return render(request, 'accounts/signup.html', context)


class LoginIn(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
            'title': "Вход"
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ob = EmailBackend()
            user, error = ob.authenticate(email=cd['email'],
                                          password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    form = LoginForm()
                    context = {
                        'form': form,
                        'error': 'Disabled account',
                        'title': 'Вход'
                    }
                    return render(request, 'accounts/login.html', context)
            else:
                form = LoginForm()
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Вход'
                }
                return render(request, 'accounts/login.html', context)


class SignOutView(LogoutView):
    next_page = '/'


class ProfileDetail(DetailView):

    model = Profile
    template = 'profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context["id_user"] = self.get_object().id
        return context
