# coding=utf-8
import datetime
from django.utils.timezone import now
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(u'Token inválido')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('Usuario inactivo o eliminado')
        utc_now = now()
        if token.created < utc_now - datetime.timedelta(days=30):
            raise exceptions.AuthenticationFailed('Token expirado')
        return token.user, token
