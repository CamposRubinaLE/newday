from django.utils.timezone import now
import django_filters
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import DjangoFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import ExpiringTokenAuthentication
from .filters import EventFilter
from .models import Category, Place, Event
from .serializers import CategorySerializer, PlaceOfUserSerializer, PlaceSerializer, EventSerializer


class ListCategoryAPI(ListAPIView):
    ''' Lista las categorias '''
    serializer_class = CategorySerializer
    # authentication_classes = ()
    # permission_classes = (AllowAny,)
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(is_enabled=True)


class ListPlaceAPI(ListAPIView):
    ''' Lista los lugares '''
    serializer_class = PlaceSerializer
    # authentication_classes = ()
    # permission_classes = (AllowAny,)
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Place.objects.filter(is_enabled=True)


class DetailPlaceAPI(RetrieveAPIView):
    ''' Detalle de Lugar pk en Url '''
    serializer_class = PlaceSerializer
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Place.objects.filter(is_enabled=True)


class ListPlacesOfUserAPI(ListAPIView):
    ''' Lista los lugares favoritos del usuario '''
    serializer_class = PlaceSerializer
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.places and len(user.places) > 0:
            return Place.objects.filter(is_enabled=True, id__in=user.places)
        else:
            return []


class AddPlacesOfUserAPI(APIView):
    ''' Agregar Lugar favorito id del lugar en el body "id_place" '''
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        place = get_object_or_404(Place.objects.filter(is_enabled=True), id=request.data.get('id_place'))
        if request.user.places and place.id in request.user.places:
            return Response({'detail': 'Not like'}, status=status.HTTP_303_SEE_OTHER)
        else:
            if request.user.places:
                request.user.places.append(place.id)
            else:
                request.user.places = [place.id]
            request.user.save()
            return Response({'detail': 'Added favorite place'}, status=status.HTTP_200_OK)


class RemovePlacesOfUserAPI(APIView):
    ''' Quita Lugar favorito id del lugar en el body "id_place" '''
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        place = get_object_or_404(Place.objects.filter(is_enabled=True), id=request.data.get('id_place'))
        if request.user.places and place.id in request.user.places:
            request.user.places.remove(place.id)
            request.user.save()
            return Response({'detail': 'Removed favorite place'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not remove'}, status=status.HTTP_303_SEE_OTHER)


class RateEventForUserAPI(APIView):
    ''' Calificar Evento POST pk in url and "val" in body'''
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event.objects.filter(is_enabled=True), id=self.kwargs.get('pk'))
        for score in event.scores:
            if self.request.user.id == score.get('id'):
                event.scores.remove({"id": score.get('id'), "val": score.get('val')})
                break
        event.scores.append({"id": request.user.id, "val": int(request.data.get('val'))})
        event.set_score()
        return Response({'detail': 'Rate the event', 'new_score': event.score}, status=status.HTTP_200_OK)


class ListEventsAPI(ListAPIView):
    ''' Lista Lugares favoritos Apartir de hoy
        para filtros
        api/events/?child=True&teen=True&adult=False&score=3&date=yyyy-mm-dd&min_price=10&max_price=20
    '''
    authentication_classes = (ExpiringTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = EventFilter

    def get_queryset(self):
        now_date = now().date()
        return Event.objects.filter(is_enabled=True, end_day__gte=now_date)
