from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import CreateUser

urlpatterns = [
    path("token/new/", TokenObtainPairView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("create/", CreateUser.as_view())
]
