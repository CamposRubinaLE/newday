from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from datetime import timedelta
from accounts.authentication import ExpiringTokenAuthentication


class TokenMixin(object):
    def regenerate(self, user):
        token, created = Token.objects.get_or_create(user=user)
        utc_now = now()
        if not created and token.created < utc_now - timedelta(days=30):
            token.delete()
            token = Token.objects.create(user=user)
        return token


class RefreshTokenMixin(object):
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.refresh()  # refresh the token
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def refresh(self):
        successful_authenticator = self.request.successful_authenticator
        if self.request.user.is_authenticated() and isinstance(successful_authenticator, ExpiringTokenAuthentication):
            token = Token.objects.filter(user=self.request.user).first()
            utc_now = now()
            if token and token.created < utc_now - timedelta(days=1):
                token.created = utc_now
                token.save()