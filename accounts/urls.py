from django.urls import path
from accounts.views import ProfileDetail
from django.conf import settings
from django.conf.urls.static import static
from .views import SignUp, LoginIn, SignOutView


urlpatterns = [
    path(r'<int:pk>', ProfileDetail.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
