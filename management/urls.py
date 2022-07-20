from django.urls import path

from management import views

app_name = "management"
urlpatterns = [
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]
