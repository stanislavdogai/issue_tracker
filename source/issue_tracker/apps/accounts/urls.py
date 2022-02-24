from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from issue_tracker.apps.accounts.views import register_view, ProfileDetailView, ProfilesView, UserChangeView, \
    UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', register_view, name='registration'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('profiles/', ProfilesView.as_view(), name='profiles'),
    path('<int:pk>/change/', UserChangeView.as_view(), name='change'),
    path('<int:pk>/change_password/', UserPasswordChangeView.as_view(), name='change_password')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)