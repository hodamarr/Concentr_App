from . import views
from django.urls import path

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup_user"),
    path("login/", views.LoginView.as_view(), name="login_user"),
    path('mod', views.CeleryTest.as_view(), name="celery_test"),
]
