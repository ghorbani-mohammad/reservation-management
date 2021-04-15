from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)

from . import models
from . import serializers
from . import filters


class RoomPagination(PageNumberPagination):
    page_size = 10


class RoomViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = models.Room.objects.order_by('-id')
    serializers = {
        'create': serializers.RoomCreateUpdateDestroySerializer,
        'list': serializers.RoomListDetailSerializer,
        'retrieve': serializers.RoomListDetailSerializer,
        'update': serializers.RoomCreateUpdateDestroySerializer,
        'destroy': serializers.RoomCreateUpdateDestroySerializer,
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RoomFilter
    pagination_class = RoomPagination

    def get_serializer_class(self):
        return self.serializers.get(self.action)


class ReservationPagination(PageNumberPagination):
    page_size = 10


class ReserveViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = models.Reservation.objects.order_by('-id')
    serializers = {
        'create': serializers.ReservationSerializer,
        'update': serializers.ReservationSerializer,
        'list': serializers.ReservationListDetailSerializer,
        'retrieve': serializers.ReservationListDetailSerializer,
    }
    pagination_class = ReservationPagination

    def get_serializer_class(self):
        return self.serializers.get(self.action)


class CheckAvailabilityAPIView(APIView):
    serializer_class = serializers.CheckAvailabilitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response(
            {'available': data['room'].available(data['start_date'], data['end_date'])}
        )
