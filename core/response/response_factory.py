from rest_framework import status
from rest_framework.response import Response

from core.response.response_builder import ResponseBuilder


class ResponseFactory:
    @staticmethod
    def create_success() -> ResponseBuilder:
        return (ResponseBuilder()
                .set_success(True)
                .set_code(status.HTTP_200_OK)
                )

    @staticmethod
    def create_error() -> ResponseBuilder:
        return (ResponseBuilder()
                .set_success(False)
                .set_code(status.HTTP_400_BAD_REQUEST)
                )