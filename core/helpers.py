from rest_framework import status
from rest_framework.response import Response

def success_response(message="", data=None, status_code=status.HTTP_200_OK):
    data = {
        "success": True,
        "message": message,
        "code": status_code,
        "data": data
    }
    return Response(data=data, status=status_code)


def error_response(message="", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    data = {
        "success": False,
        "message": message,
        "code": status_code,
        "data": data
    }
    return Response(data=data, status=status_code)