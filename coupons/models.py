# encoding=utf-8
from __future__ import unicode_literals
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from hashids import Hashids
import qrcode
from django.db import models


# Create your models here.
from accounts.models import User
from events.models import Event


class Company(models.Model):
    name = models.CharField(max_length=400)
    logo = models.ImageField(upload_to='companies/logos', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Empresas privadas"
        verbose_name = "Empresa privada"
        ordering = ['name']

    def __unicode__(self):
        return u'{}'.format(self.name)


class Coupon(models.Model):
    company = models.ForeignKey(Company, related_name='coupons', verbose_name='Empresa Privada')
    event = models.ForeignKey(Event, related_name='coupons', verbose_name='Evento')
    valid = models.CharField(max_length=500, verbose_name='Fechas del cupon',
                             help_text='Lunes 01 Nov - Jueves 31 Dic 2016')
    image = models.ImageField(upload_to='coupons/images', verbose_name='Imagen del cupon')
    description = models.TextField(blank=True, verbose_name='Detalle del cupon')
    code = models.CharField(max_length=10, verbose_name="Código", null=True, blank=True)
    qr_code = models.ImageField(upload_to='coupons/qrs', blank=True, null=True)
    terms_conditions = models.TextField(blank=True, verbose_name='terminos y condiciones')
    users = models.ManyToManyField(User, related_name='coupons', through='CouponUser')
    q_1 = models.CharField(max_length=300, verbose_name='Opcion 1')
    q_2 = models.CharField(max_length=300, verbose_name='Opcion 2')
    q_3 = models.CharField(max_length=300, verbose_name='Opcion 3')
    q_4 = models.CharField(max_length=300, verbose_name='Opcion 4')
    a_1 = models.PositiveIntegerField(verbose_name='Respuesta', default=1)
    question = models.CharField(verbose_name='Pregunta', default='', max_length=500)

    class Meta:
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Coupon, self).save()
        if self.pk and not self.code:
            HASHIDS = Hashids(salt='Coupon', min_length=10)
            self.code = HASHIDS.encode(self.pk)
            if not self.qr_code:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )
                data = '{}'.format(self.code)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image()
                buffer = BytesIO()
                img.save(buffer)
                filename = 'cupondetailqrcode-%s.png' % self.pk
                filebuffer = InMemoryUploadedFile(
                    buffer, None, filename, 'image/png', None, None)
                self.qr_code.save(filename, filebuffer)
                super(Coupon, self).save(update_fields=['code', 'qr_code'])
            super(Coupon, self).save(update_fields=['code'])

    def __str__(self):
        return self.code


class CouponUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons_user')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupons_user')
    qr_code = models.ImageField(upload_to='coupons_user/qrs', blank=True, null=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.user, self.coupon)

    class Meta:
        verbose_name = 'Cupon Usuario'
        verbose_name_plural = 'Cupones Usuario'
        unique_together = ('user', 'coupon')
        ordering = ['-created_at']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(CouponUser, self).save()
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            data = 'cupon:{} - user:{}'.format(self.coupon.code, self.user.code)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer)
            filename = 'valeqrcode-%s.png' % self.pk
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', None, None)
            self.qr_code.save(filename, filebuffer)
            super(CouponUser, self).save(update_fields=['qr_code'])
