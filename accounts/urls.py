from django.urls import path
from .views import SignUp, ProfileDetail, LoginIn, SignOutView, ProfileUpdateView


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginIn.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
]
