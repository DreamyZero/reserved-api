from rest_framework import serializers

from reservation.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'groups', 'user_permissions')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Table
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()
    served = UserSerializer()

    class Meta:
        model = ReservationHistory
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'author', 'description', 'created_at')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
