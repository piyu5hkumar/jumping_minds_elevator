from django.urls import include, path
from rest_framework import routers
from elevator import views

router = routers.DefaultRouter()
router.register("elevators", views.ElevatorViewSet, basename="elevators")
router.register("requests", views.UserRequestViewSet, basename="requests")

urlpatterns = [
    path("", include(router.urls)),
]
