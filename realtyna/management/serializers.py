from rest_framework.serializers import ModelSerializer
from datetime import timedelta
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
