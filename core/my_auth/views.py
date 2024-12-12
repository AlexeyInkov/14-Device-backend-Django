from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserTokenSerializer, UserOrganizationSerializer


class UserMeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserOrganizationSerializer

    def get(self, request):
        # token = request.META.get('Authorization')
        # if token:
        #     token = token.split(' ')[1]
        #     user_id = Token.objects.get(key=token).user
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        if user.is_authenticated:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginAPIView(CreateAPIView):
    serializer_class = UserTokenSerializer

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.data.get("username")
            password = request.data.get("password")

            user = None
            if "@" in username:
                try:
                    user = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    pass

            if not user:
                user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                data = {
                    "token": token.key,
                }
                # request.META["Authorization"] = f"Token {token}"
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            request.headers.pop("Authorization")
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
