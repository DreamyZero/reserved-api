# Create your views here.
from datetime import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from reservation.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['client', 'phone']
    ordering_fields = ['count', 'created_at', 'visit_date', 'visit_time']
    filter_fields = ['is_finishing', 'table']

    @action(methods=['get'], detail=False)
    def today(self, request):
        reservations = Reservation.objects.filter(Q(visit_date=datetime.now())
                                                  & Q(visit_time__gt=datetime.now())
                                                  & Q(is_finishing=False))

        reservation_serializer = ReservationSerializer(reservations, many=True)
        return Response(reservation_serializer.data)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['description']
    ordering_fields = ['capacity']
    filter_fields = ['is_reserved', 'category']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name', 'description']


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = ReservationHistory.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['total', 'visited_at']
    filter_fields = ['served']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['description', 'author']
    ordering_fields = ['created_at']
    filter_fields = ['reservation_history']

    @action(methods=['get'], detail=True)
    def history(self, request, pk=None):
        history = Review.objects.get(pk=pk).reservation_history
        history_serializer = HistorySerializer(history)

        return Response(history_serializer.data)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['phone', 'name']
    ordering_fields = ['created_at', 'visit_date', 'visit_time', 'count']
    filter_fields = ['archived']

    @action(methods=['post'], detail=True)
    def accept(self, request, pk=None):
        table_id = request.POST['table']

        if not Request.objects.filter(pk=pk).exists():
            raise serializers.ValidationError('Запроса с таким ID не существует.')
        if not Table.objects.filter(pk=table_id).exists():
            raise serializers.ValidationError('Столика с таким ID не существует.')

        request_ = Request.objects.get(pk=pk)

        if request_.archived:
            raise serializers.ErrorDetail('Данный запрос уже обработан.')

        request_.archived = True

        table = Table.objects.get(pk=table_id)

        if table.is_reserved:
            raise serializers.ErrorDetail('Столик с таким ID уже забронирован.')

        table.is_reserved = True

        reservation = Reservation.objects.create(
            visit_date=request_.visit_date,
            visit_time=request_.visit_time,
            count=request_.count,
            table_id=table_id,
            client=request_.name,
            phone=request_.phone
        )

        reservation_serializer = ReservationSerializer(reservation)
        return Response(reservation_serializer.data)

    @action(methods=['get'], detail=True)
    def reject(self, request, pk=None):
        if not Request.objects.filter(pk=pk).exists():
            raise serializers.ValidationError('Запроса с таким ID не существует.')

        request_ = Request.objects.get(pk=pk)

        if request_.archived:
            raise serializers.ErrorDetail('Данный запрос уже обработан.')

        request_.archived = True

        request_serializer = RequestSerializer(request_)
        return Response(request_serializer.data)

    @action(methods=['get'], detail=False)
    def archived(self, request):
        requests = Request.objects.filter(archived=False)

        request_serializer = RequestSerializer(requests, many=True)
        return Response(request_serializer.data)
