from django_filters import rest_framework as filters
from . import models


class RoomFilter(filters.FilterSet):
    owner = filters.CharFilter(
        field_name="owner__username",
        lookup_expr='iexact',
    )

    class Meta:
        model = models.Room
        fields = ('owner',)


class ReservationFilter(filters.FilterSet):
    owner = filters.CharFilter(
        field_name="room__owner__username",
        lookup_expr='iexact',
    )

    class Meta:
        model = models.Reservation
        fields = ('owner',)