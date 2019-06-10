from rest_framework.routers import DefaultRouter

from api.v1.views import UserViewSet

router = DefaultRouter()

router.register(r'user', UserViewSet, base_name='user')

urlpatterns = router.urls
