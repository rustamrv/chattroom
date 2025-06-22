from django.urls import path
from .views import HomePage, RoomList, ChatDetail, My_Room, RoomCreate


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('rooms/', RoomList.as_view(), name='room'),
    path('rooms/create/', RoomCreate.as_view(), name='create_room'),
    path('my_rooms/', My_Room.as_view(), name='my_room'),
    path('chats/<int:pk>/', ChatDetail.as_view(), name='detail'),
]