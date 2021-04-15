from rest_framework.serializers import ModelSerializer
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
