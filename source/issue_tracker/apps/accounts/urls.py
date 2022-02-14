from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from issue_tracker.apps.accounts.views import register_view

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', register_view, name='registration')
]