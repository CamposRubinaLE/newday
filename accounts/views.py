from django.db import transaction
from django.utils.decorators import method_decorator
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from social.apps.django_app.utils import psa
from rest_framework.response import Response
from .authentication import ExpiringTokenAuthentication
from .mixins import TokenMixin, RefreshTokenMixin
from .models import User
from .serializers import LoginSerializer, RegisterUserSerializer, UserProfileSerializer


class FacebookLoginAPI(TokenMixin, APIView):
    @method_decorator(psa('accounts:facebook-complete'))
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookLoginAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        token = request.data.get('access_token')
        try:
            user = request.backend.do_auth(token)
        except HTTPError, ex:
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: ["Invalid facebook token"]})
        token = self.regenerate(user)
        return Response({'token': token.key, 'id_user': user.id}, status=status.HTTP_200_OK)


class RetrieveUpdateUserProfileAPI(RefreshTokenMixin, RetrieveUpdateAPIView):
    ''' Detalle del User '''
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserRegisterAPI(CreateAPIView):
    '''Registro de Nuevos Usuarios'''
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(UserRegisterAPI, self).dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(email=serializer.validated_data.get('email')).exists():
            user = self.perform_create(serializer)
            token, created = Token.objects.get_or_create(user=user)
            headers = self.get_success_headers(serializer.data)
            user_serializer = RegisterUserSerializer(user, context={"request": request})
            return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK,
                            headers=headers)
        else:
            return Response({"detail": 'Correo ya registrado'}, status=status.HTTP_303_SEE_OTHER)


class LoginAPI(TokenMixin, APIView):
    ''' Login Fields : email,password '''

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        token = self.regenerate(user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
