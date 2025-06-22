from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.views import View
from .models import Profile
from feed.models import Post
from feed.forms import PostForm
from django.utils import timezone
from django.views.generic import UpdateView, DetailView
from .forms import UpdateForm
from django.contrib.auth.views import LogoutView 
from django.urls import reverse_lazy
import redis  
import project.settings as setting

redis_instance = redis.StrictRedis(host=setting.REDIS_HOST,
                                   port=setting.REDIS_PORT, db=0)


class SignUp(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        context = {
            'form': form,
            'title': "Sign Up"
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            user = form.save() 
            ob = Profile.objects.get(id=user.id)        
            ob.is_active = True
            ob.save() 
            return redirect("login")
        else:
            error = form.errors.as_json()
            form = SignUpForm() 
            context = {
                'form': form,
                'error': error,
                'title': "Sign Up"
            }
            return render(request, 'accounts/signup.html', context)


class LoginIn(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
            'title': "Login"
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
                        'title': 'Login'
                    }
                    return render(request, 'accounts/login.html', context)
            else:
                form = LoginForm()
                context = {
                    'form': form,
                    'error': 'Incorrect login or password',
                    'title': 'Login'
                }
                return render(request, 'accounts/login.html', context)


class SignOutView(LogoutView):
    next_page = '/'


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = UpdateForm
    template_name = 'accounts/profile_form.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class ProfileDetail(DetailView):

    model = Profile
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        context['posts'] = Post.objects.filter(author=self.get_object()).order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.name = f"Post by {post.author}"
            post.save()
            return redirect('profile', pk=self.kwargs['pk'])
        else:
            return self.get(request, *args, **kwargs)
