from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, SuccessTokenForm
from django.views import View
from .models import Profile, Post
from django.utils import timezone
from django.views.generic import UpdateView, DetailView
from .forms import UpdateForm
from django.contrib.auth.views import LogoutView 
import redis  
import project.settings as setting

redis_instance = redis.StrictRedis(host=setting.REDIS_HOST,
                                   port=setting.REDIS_PORT, db=0)


class SuccessToken(View):
    
    def post(self, request, *args, **kwargs):
        form = SuccessTokenForm(request.POST)
        if form.is_valid():   
            recip = request.session.get('email')
            token = request.POST['token']  
            value = redis_instance.get(recip)
            value = value.decode(encoding='UTF-8')  
            if value == token:
                ob = EmailBackend()
                result, user = ob.get_user_email(recip, True)
                if result: 
                    auth_login(request, user)
                    return redirect('home') 
                else:
                    return redirect('home')
            else:
                return redirect('home')

    def get(self, request, *args, **kwargs):
        form = SuccessTokenForm()
        context = {
            'form': form,
            'title': "Завершенние регистрация"
        } 
        return render(request, 'accounts/success_token.html', context)

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
            ob = Profile.objects.get(id=user.id)        
            ob.is_active = False
            ob.save() 
            request.session['email'] = request.POST['email'] 
            return redirect("success")
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
            user = authenticate(email=cd['email'], password=cd['password']) 
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
                    'error': 'Не правильный логин или пароль',
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
        context["posts"] = Post.objects.filter(recipient=self.get_object())
        return context
