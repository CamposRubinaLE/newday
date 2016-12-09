from django.conf.urls import url
from .views import ListCategoryAPI, ListPlacesOfUserAPI, AddPlacesOfUserAPI, RemovePlacesOfUserAPI, DetailPlaceAPI, \
    ListPlaceAPI, ListEventsAPI, RateEventForUserAPI

urlpatterns = [
    url(r'^api/categories/$', ListCategoryAPI.as_view(), name="list-categories"),
    url(r'^api/places/$', ListPlaceAPI.as_view(), name="list-places"),  # GET
    url(r'^api/places/(?P<pk>\d+)/$', DetailPlaceAPI.as_view(), name="detail-place"),  # GET pk of place in url
    url(r'^api/event/(?P<pk>\d+)/rate/$', RateEventForUserAPI.as_view(),
        name="rate-event"),  # POST pk in url and "val" in body
    url(r'^api/me/places/$', ListPlacesOfUserAPI.as_view(), name="list-me-places"),
    url(r'^api/me/places/add/$', AddPlacesOfUserAPI.as_view(), name="add-me-places"),  # Post id_places
    url(r'^api/me/places/remove/$', RemovePlacesOfUserAPI.as_view(), name="remove-me-places"),
    # Post "id_places" in body
    url(r'^api/events/$', ListEventsAPI.as_view(), name="list-events"),  # GET

]
