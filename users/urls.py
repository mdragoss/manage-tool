from django.urls import include, path

from .views import LogInView, LogOutView, RegisterView, UserView

user_routes = [
    path('auth/login/', LogInView.as_view()),
    path('auth/logout/', LogOutView.as_view()),
    path('auth/user/', UserView.as_view()),
    path('auth/register/', RegisterView.as_view()),
]
