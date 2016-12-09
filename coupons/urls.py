from django.conf.urls import url
from coupons.views import DetailCouponAPI, QualifyTriviaAPI, ListMyCuponsAPI

urlpatterns = [
    url(r'^api/cupons/(?P<code>\w+)/$', DetailCouponAPI.as_view(), name='cupon-detail'),
    url(r'^api/cupons/(?P<pk>\d+)/qualify/$', QualifyTriviaAPI.as_view(), name='cupon-qualify'),
    url(r'^api/me/cupons/$', ListMyCuponsAPI.as_view(), name='cupon-list-my'),
]
