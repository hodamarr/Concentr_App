from django.shortcuts import render
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .token import create_jwt_pair_for_user
from django.http import HttpResponse
from rest_framework.decorators import api_view
from concentrApp.tasks import update_celery_beat_schedule


class CeleryTest(generics.GenericAPIView):
    authentication_classes = []  # remove authentication requirement
    permission_classes = [AllowAny]  # allow any user to access the view

    def get(self, request):
        x, y = int(request.query_params.get('x')), int(request.query_params.get('y'))
        from application.models import Schedule
        update_celery_beat_schedule(Schedule.objects.first())
        return HttpResponse(f'Success !')


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializers
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data={"message": "user created successfully",
                                  "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            # for reguealr token return user.auth_token.key
            resp = {
                "message": "success",
                "token": tokens
            }
            return Response(data=resp, status=status.HTTP_200_OK)
        return Response(
            data={
                "message": "invalid email or password"},
            status=status.HTTP_404_NOT_FOUND)
