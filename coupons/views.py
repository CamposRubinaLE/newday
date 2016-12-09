from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404, GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.authentication import ExpiringTokenAuthentication
from .models import Coupon, CouponUser
from serializers import DetailCouponSerializer, ListMyCouponsSerializer


class DetailCouponAPI(RetrieveAPIView):
    ''' Detalle de cupon Qr o por api enviar "code" en url    '''
    # authentication_classes = ()
    # permission_classes = (AllowAny,)
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DetailCouponSerializer

    def get_object(self):
        return get_object_or_404(Coupon.objects.all(), code=self.kwargs.get('code'))


class QualifyTriviaAPI(ListModelMixin, GenericAPIView):
    ''' Calificar la trivia pk de Cupon en url y "approved" en el body
        ejemplo 1 si responde 3 preguntas correctas, 0 si no...
    '''
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        coupon = get_object_or_404(Coupon.objects.all(), id=self.kwargs.get('pk'))
        approved = eval(request.data.get('approved'))
        if approved:
            CouponUser.objects.create(user=self.request.user, coupon=coupon)
            return self.list(request, *args, **kwargs)
        else:
            return Response({'detail': "No pasaste la Trivia. Vuelve a intentarlo"}, status=status.HTTP_303_SEE_OTHER)

    def list(self, request, *args, **kwargs):
        queryset = self.request.user.coupons_user.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListMyCouponsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ListMyCouponsSerializer(queryset, many=True)
        return Response(serializer.data)


class ListMyCuponsAPI(ListAPIView):
    '''List mys cupones agregados '''
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListMyCouponsSerializer

    def get_queryset(self):
        return self.request.user.coupons_user.all()
