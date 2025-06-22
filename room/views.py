from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Room, MembersRoom, Message
from django.views import View
from accounts.models import Profile
from .forms import RoomForm
from django.urls import reverse_lazy


class HomePage(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context["title"] = "Chat Room"
        context["id_user"] = self.request.session.get('_auth_user_id')
        return render(request, 'home/home.html', context=context)


class RoomCreate(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'room/room_form.html'
    success_url = reverse_lazy('room')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RoomList(ListView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context["title"] = "Chattroom - All rooms"
        context['rooms'] = Room.objects.all() 
        context["id_user"] = self.request.session.get('_auth_user_id')
        return context


class My_Room(View):

    def get(self, request, *args, **kwargs):
        context = {}
        id = self.request.session.get('_auth_user_id')
        user = Profile.objects.get_id(id) 
        context["id_user"] = id
        context["title"] = "Chattroom - My rooms"
        context['rooms'] = Room.objects.get_myroom(user)
        return render(request, 'room/room_list.html', context=context)


class ChatDetail(DetailView):

    model = Room
    template_name = 'room/room_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        id = self.request.session.get('_auth_user_id')
        user = Profile.objects.get_id(id)
        is_member = MembersRoom.objects.get_member_room(user, self.get_object())
        context['messages'] = Message.objects.all().filter(room=self.get_object())
        context["rooms"] = Room.objects.get_public()
        context["id_user"] = id
        context['is_member'] = is_member
        return context
