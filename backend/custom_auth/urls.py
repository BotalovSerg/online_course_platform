from django.urls import path

from .views import LoginView

urlpatterns = [
    path("token/", LoginView.as_view(), name="login"),
]
