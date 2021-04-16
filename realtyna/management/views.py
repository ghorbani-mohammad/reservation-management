from django.http import HttpResponse
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ReservationFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        res = ''
        print(response.data['results'])
        for item in response.data['results']:
            res += f'<div style="margin-top:1px;border:solid;padding:1px;">Reservation Name: \
                {item["name"]} <br>Room Id: {item["room"]["id"]} <br>Room Owner: {item["room"]["owner"]["username"]} \
                <br>Start Date: {item["start_date"]} <br>End Date: {item["end_date"]}</div>'
        html = f'<html><body>{res}</body></html>'
        return HttpResponse(html)

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


class CheckNumberAvailabilityAPIView(APIView):
    serializer_class = serializers.CheckNumberRoomAvailabilitySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rooms = models.Room.objects.all()
        room_counter = 0
        bed_counter = 0
        for room in rooms:
            if room.available(data['start_date'], data['end_date']):
                room_counter += 1
                bed_counter += room.bed

        return Response(
            {
                'available_requested_rooms': True
                if room_counter >= data['number']
                else False,
                'available_rooms_count': room_counter,
                'available_beds_count': bed_counter,
            }
        )
