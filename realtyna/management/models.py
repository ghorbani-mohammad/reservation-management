from django.db import models
from django.core.validators import MinValueValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(BaseModel):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.username


class Room(BaseModel):
    bed = models.IntegerField(default=1)
    owner = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.pk}. {self.owner}'


class Reservation(BaseModel):
    room = models.ForeignKey(Room, related_name='reserves', on_delete=models.CASCADE)
    reserver = models.ForeignKey(
        User, related_name='reservations', on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    duration = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    end_date = models.DateTimeField()