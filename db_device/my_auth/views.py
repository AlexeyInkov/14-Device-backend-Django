from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from metering_unit.models import Organization
from metering_unit.serializers import OrganizationSerializer
from .serializers import UserSerializer


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
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
                queryset = Organization.objects.prefetch_related("user_to_org").filter(
                    user_to_org__user=user.id
                )
                data = {
                    "id": user.id,
                    "username": user.username,
                    "token": token.key,
                    "organizations": OrganizationSerializer(queryset, many=True).data,
                }
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
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
