from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('room', views.RoomViewSet, basename='room')
urlpatterns = []

urlpatterns += router.urls
