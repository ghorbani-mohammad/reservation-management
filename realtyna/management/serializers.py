from datetime import timedelta

from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ValidationError

from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'id',
            'username',
        )


class RoomCreateUpdateDestroySerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['owner'] = UserSerializer(instance.owner).data
        return data

    class Meta:
        model = models.Room
        fields = (
            'id',
            'bed',
            'owner',
        )


class RoomListDetailSerializer(ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = models.Room
        fields = (
            'id',
            'bed',
            'owner',
            'in_reserve',
        )


class ReservationSerializer(ModelSerializer):
    def validate(self, data):
        if not 'end_date' in data:
            data['end_date'] = data['start_date'] + timedelta(days=data['duration'])
        if data['room'].in_reserve:
            raise ValidationError({"room": "room is reserved"})
        if not data['room'].available(data['start_date'], data['end_date']):
            raise ValidationError({"room": "room is not available"})
        if data['start_date'] < timezone.localtime():
            raise ValidationError({"start_date": "start must occur after now"})
        return data

    def create(self, validated_data):
        obj = models.Reservation(**validated_data)
        obj.save()
        return obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['room'] = RoomListDetailSerializer(instance.room).data
        data['reserver'] = UserSerializer(instance.reserver).data
        return data

    class Meta:
        model = models.Reservation
        fields = (
            'id',
            'name',
            'room',
            'reserver',
            'start_date',
            'duration',
            'end_date',
        )
        extra_kwargs = {'end_date': {'required': False}, 'name': {'required': True}}


class CheckAvailabilitySerializer(ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = (
            'room',
            'start_date',
            'end_date',
        )
