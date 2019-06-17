from rest_framework.routers import DefaultRouter

from api.v1.views import (
    UserViewSet,
    ReservationViewSet,
    AvailableFlightsViewSet,
)

router = DefaultRouter()

router.register(r'user', UserViewSet, base_name='user')
router.register(
    r'available_flights', AvailableFlightsViewSet,
    base_name='available_flights')
router.register(r'reservation', ReservationViewSet, base_name='reservation')

urlpatterns = router.urls
