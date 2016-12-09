from .views import LoginAPI, UserRegisterAPI, RetrieveUpdateUserProfileAPI, FacebookLoginAPI
from social.apps.django_app.views import complete
from django.conf.urls import url

urlpatterns = [
    url(r'^api/login/$', LoginAPI.as_view(), name="login"),
    url(r'^api/register/$', UserRegisterAPI.as_view(), name="register"),
    url(r'^api/me/$', RetrieveUpdateUserProfileAPI.as_view(), name="retrieve-profile"),
    url(r'^api/login/(?P<backend>[^/]+)/$', FacebookLoginAPI.as_view(), name='facebook-login'),
    url(r'^api/complete/(?P<backend>[^/]+)/$', complete, name='facebook-complete'),

]
