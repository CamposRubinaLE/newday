from django.contrib import admin

# Register your models here.
from .models import Company, Coupon, CouponUser

admin.site.register(Company)
admin.site.register(Coupon)
admin.site.register(CouponUser)
