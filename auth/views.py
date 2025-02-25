from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.helpers import error_response, success_response
from core.response.response_factory import ResponseFactory
from posinventoryapi import settings
from .serializers import LoginSerializer, RefreshSerializer


# Create your views here.
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return (ResponseFactory
                    .create_error()
                    .set_code(status.HTTP_401_UNAUTHORIZED)
                    .set_message("Invalid username or password.")
                    .build()
                    )

        username, password = (serializer.validated_data['username'],
                              serializer.validated_data['password'])
        user = authenticate(username=username, password=password)

        if user is None:
            return (ResponseFactory
                    .create_error()
                    .set_code(status.HTTP_401_UNAUTHORIZED)
                    .set_message("Invalid username or password.")
                    .build()
                    )

        refresh_token = RefreshToken.for_user(user)

        response = (
            ResponseFactory
            .create_success()
            .set_message(f"Welcome back, {user.username}! You’re now logged in.")
            .set_data({
                "id": user.id,
                "username": user.username,
                "email": user.email
            })
            .set_cookie({"access_token": str(refresh_token.access_token)})
            .set_cookie({"refresh_token": str(refresh_token)})
            .build()
        )

        return response

class LogoutAPIView(APIView):
    def post(self):
        response = success_response(message="Logout successfully!")

        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie("refresh_token")

        return response

class RefreshAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RefreshSerializer(request.COOKIES)

        try:
            if not serializer.is_valid(raise_exception=True):
                return success_response(
                    message="Refresh token is required.",
                    status_code=status.HTTP_200_OK
                )
            return success_response(
                message="Refresh token is successfully refreshed.",
                status_code=status.HTTP_200_OK
            )
        except TokenError:
            return error_response(
                message="Refresh token is invalid or expired.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

