from django.urls import path
from .views import LoginAPIView, LogoutAPIView, RefreshAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
]