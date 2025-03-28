from rest_framework.response import Response
from posinventoryapi import settings


class ResponseBuilder:
    success = False
    message = ""
    code = 0
    data = None

    cookies = []

    def set_success(self, success) -> "ResponseBuilder":
        self.success = success
        return self

    def set_message(self, message) -> "ResponseBuilder":
        self.message = message
        return self

    def set_code(self, code) -> "ResponseBuilder":
        self.code = code
        return self

    def set_data(self, data) -> "ResponseBuilder":
        self.data = data
        return self

    def set_cookie(self, cookie) -> "ResponseBuilder":
        self.cookies.append(cookie)
        return self

    def build(self) -> Response:
        data = {
            "success": self.success,
            "message": self.message,
            "code": self.code,
            "data": self.data
        }

        response = Response(data=data, status=self.code)
        cookies = { k: v for cookie in self.cookies for k, v in cookie.items() }

        for key, value in cookies.items():
            response.set_cookie(
                key=key,
                value=value,
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"]
            )

        return response