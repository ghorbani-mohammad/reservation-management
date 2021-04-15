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
        )


class ReservationSerializer(ModelSerializer):
    def validate(self, data):
        print(data['room'].in_reserve)
        if data['room'].in_reserve:
            raise ValidationError({"room": "room is reserved"})
        if data['start_date'] < timezone.localtime():
            raise ValidationError({"start_date": "start must occur after now"})
        return data

    def create(self, validated_data):
        obj = models.Reservation(**validated_data)
        obj.end_date = obj.start_date + timedelta(days=obj.duration)
        obj.save()
        return obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['room'] = RoomListDetailSerializer(instance.room).data
        data['reserver'] = UserSerializer(instance.reserver).data
        return data

    class Meta:
        model = models.Reservation
        fields = ('id', 'room', 'reserver', 'start_date', 'duration', 'end_date')
        extra_kwargs = {'end_date': {'required': False}}
