from rest_framework.pagination import PageNumberPagination

__author__ = 'lucaru9'


class Pagination(PageNumberPagination):
    page_size = 10
