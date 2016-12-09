# coding=utf-8
from __future__ import unicode_literals
from __future__ import division
from django.db import models
from django_pg.models import JSONField
from accounts.models import User


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, verbose_name='Nombre')
    is_enabled = models.BooleanField(default=True, verbose_name='Habilitado',
                                     help_text='Habilitar o deshabilitar Categoria')
    image = models.FileField(upload_to='category/files', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"
        ordering = ['name']

    def __unicode__(self):
        return u'{}'.format(self.name)


class Place(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, verbose_name='Nombre')
    address = models.CharField(max_length=500, verbose_name='Dirección')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Longitud', null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='Latitud', null=True, blank=True)
    is_enabled = models.BooleanField(default=True, verbose_name='Habilitado',
                                     help_text='Habilitar o deshabilitar lugar')
    file_1 = models.FileField(upload_to='places/file', null=True, blank=True)
    file_2 = models.FileField(upload_to='places/file', null=True, blank=True)
    file_3 = models.FileField(upload_to='places/file', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Lugares"
        verbose_name = "Lugar"
        ordering = ['name']

    def __unicode__(self):
        return u'{}'.format(self.name)


class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, verbose_name='Nombre')
    is_enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    image_1 = models.FileField(upload_to='events/image', null=True, blank=True)
    image_2 = models.FileField(upload_to='events/image', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_day = models.DateField(null=True, blank=True, verbose_name='Dia inicio')
    end_day = models.DateField(null=True, blank=True, verbose_name='Dia fin')
    start_hour = models.TimeField(null=True, blank=True, verbose_name='Hora inicio')
    end_hour = models.TimeField(null=True, blank=True, verbose_name='Hora Fin')
    min_price = models.FloatField(blank=True, default=0.0)
    is_free = models.BooleanField(default=False, verbose_name='Gratis')
    prices = models.TextField(blank=True, verbose_name='Descripcion de los precios')
    for_child = models.BooleanField(default=False)
    for_teen = models.BooleanField(default=False)
    for_adult = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    scores = JSONField(default=[])
    place = models.ForeignKey(Place, null=True, blank=True, related_name='events')
    category = models.ForeignKey(Category, null=True, blank=True, related_name='events')

    class Meta:
        verbose_name_plural = "Eventos"
        verbose_name = "Evento"
        ordering = ['-created_at']

    def __unicode__(self):
        return u'{}'.format(self.name)

    def set_score(self):
        if len(self.scores) > 0:
            acu = 0
            for score in self.scores:
                acu += int(score['val'])
            self.score = round(acu / len(self.scores), 1)
        else:
            self.score = 0.0
        self.save()
