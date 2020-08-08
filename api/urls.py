from django.urls import path, include
from .views import PostCreateView, PostListView, PostDetailView, SnippetDetail

urlpatterns = [
    path('post/create/', PostCreateView.as_view()),
    path('post/all/', PostListView.as_view()),
    path('post/detail/<int:pk>', PostDetailView.as_view()),
    path('auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', SnippetDetail.as_view()),
] 
