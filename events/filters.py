from django.utils.dateparse import parse_date
from .models import Event

__author__ = 'lucaru9'
import django_filters


class EventFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name="min_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(name="min_price", lookup_expr='lte')
    child = django_filters.BooleanFilter(name="for_child")
    teen = django_filters.BooleanFilter(name="for_teen")
    adult = django_filters.BooleanFilter(name="for_adult")
    score = django_filters.NumberFilter(name="score", lookup_expr='gte')
    date = django_filters.DateFilter(method='filter_date')

    class Meta:
        model = Event
        fields = ['child', 'teen', 'adult', 'score', 'date', 'min_price', 'max_price']

    def filter_date(self, qs, name, value):
        return qs.filter(start_day__lte=value, end_day__gte=value)
