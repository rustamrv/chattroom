from django.urls import path
from .views import HomePage, RoomList


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('rooms', RoomList.as_view(), name='room'),
]
