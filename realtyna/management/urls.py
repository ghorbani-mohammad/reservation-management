from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('room', views.RoomViewSet, basename='room')
router.register('reservation', views.ReserveViewSet, basename='reservation')
urlpatterns = []

urlpatterns += router.urls
