from django.urls import path
from accounts.views import ProfileDetail
from django.conf import settings
from django.conf.urls.static import static
from .views import SignUp, LoginIn, SignOutView


urlpatterns = [
    path(r'/signup/', SignUp.as_view(), name='signup'),
    path(r'/login/', LoginIn.as_view(), name='login'),
    path(r'/logout/', SignOutView.as_view(), name='logout'),
    path(r'<int:pk>', ProfileDetail.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
