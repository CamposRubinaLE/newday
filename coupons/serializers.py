from rest_framework import serializers
from accounts.serializers import UserProfileSerializer
from .models import Coupon, CouponUser

__author__ = 'lucaru9'


class DetailCouponSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'company', 'valid', 'image', 'description', 'terms_conditions', 'q_1', 'q_2',
                  'q_3', 'q_4', 'a_1', 'question']


class ListMyCouponsSerializer(serializers.ModelSerializer):
    coupon = DetailCouponSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = CouponUser
        fields = ['id', 'created_at', 'user', 'coupon', 'qr_code', 'used']
