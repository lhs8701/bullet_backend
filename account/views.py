from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.response import Response


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
    """
    post에 성공하면 UserSerializer에 명시된 user와 token을 반환
    """


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
