from django.urls import path

from .views import RegisterUserAPIView, UserDetailAPI

app_name = "management"
urlpatterns = [
    path("user/<int:pk>", UserDetailAPI.as_view()),
    path("register", RegisterUserAPIView.as_view()),
]
