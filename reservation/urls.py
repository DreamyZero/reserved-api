from django.urls import path
from rest_framework import routers
from reservation.views import *


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('reservations', ReservationViewSet, 'reservations')
router.register('tables', TableViewSet, 'tables')
router.register('categories', CategoryViewSet, 'categories')
router.register('history', HistoryViewSet, 'history')
router.register('reviews', ReviewViewSet, 'reviews')
router.register('request', RequestViewSet, 'requests')

urlpatterns = router.urls