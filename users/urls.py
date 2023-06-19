from django.urls import path
from users.views import UserBusterView, LoginBusterView, UserByIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("users/",UserBusterView.as_view()),
    path("users/<int:user_id>/",UserByIdView.as_view()),
    path("users/refresh/", TokenRefreshView.as_view()),

    path("users/login/", TokenObtainPairView.as_view()),
]
