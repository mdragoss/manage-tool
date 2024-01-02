from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (
    LogInSerializer,
    LogOutSerializer,
    RegisterSerializer,
    UserSerializer,
)


# Create your views here.
class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
    permission_classes = (AllowAny,)


class LogOutView(GenericAPIView):
    serializer_class = LogOutSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        methods=['POST'],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={200: RegisterSerializer, 400: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = self.get_serializer(data=request_data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            # data = serializer.data
            data={
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )


class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(email=self.request.user.email)

    @extend_schema(responses=UserSerializer)
    def get(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = UserSerializer(instance=instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=UserSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(responses=UserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
