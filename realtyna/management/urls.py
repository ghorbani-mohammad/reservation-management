from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('room', views.RoomViewSet, basename='room')
router.register('reservation', views.ReserveViewSet, basename='reservation')
urlpatterns = [
    path('check_availability/', views.CheckAvailabilityAPIView.as_view()),
    path(
        'check_number_room_availability/',
        views.CheckNumberAvailabilityAPIView.as_view(),
    ),
]

urlpatterns += router.urls
