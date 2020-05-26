from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Room
from django.views import View


class HomePage(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context["title"] = "Чат комната"
        return render(request, 'room/room_list.html', context=context)


class RoomList(ListView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Rooms all"
        context['rooms'] = Room.objects.all()
        return context
