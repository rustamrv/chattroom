from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Room, MembersRoom, Message
from django.views import View
from accounts.models import Profile


class HomePage(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context["title"] = "Чат комната"
        return render(request, 'home/home.html', context=context)


class RoomList(ListView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.session.get('_auth_user_id')
        context["title"] = "Чат комната - все комнаты"
        context['rooms'] = Room.objects.all() 
        context["id_user"] = id
        return context


class My_Room(View):

    def get(self, request, *args, **kwargs):
        context = {}
        id = self.request.session.get('_auth_user_id')
        user = Profile.objects.get_id(id) 
        context["id_user"] = id
        context["title"] = "Чат комната - мои комнаты"
        context['rooms'] = Room.objects.get_myroom(user)
        return render(request, 'room/room_list.html', context=context)


class ChatDetail(DetailView):

    model = Room
    template = 'chat_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        id = self.request.session.get('_auth_user_id')
        user = Profile.objects.get_id(id)
     
        is_member = MembersRoom.objects.get_member_room(user, obj)
        context['messages'] = Message.objects.all().filter(room=obj) 
        context["rooms"] = Room.objects.get_public()
        context["id_user"] = id
        context['is_member'] = is_member
        return context