from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Table(models.Model):
    description = models.CharField(max_length=256, verbose_name='Описание')
    capacity = models.IntegerField(verbose_name='Вместимость')
    category = models.ManyToManyField('Category', verbose_name='Категория')
    is_reserved = models.BooleanField(default=False, verbose_name='Зарезервирован/Занят')

    def __str__(self):
        return 'Столик #' + str(self.pk) + '(' + str(self.capacity) + ' чел.)'

    def get_absolute_url(self):
        return reverse('table', kwargs={'table_id': self.pk})

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    description = models.CharField(max_length=64, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    visit_date = models.DateField(verbose_name='Дата посещения')
    visit_time = models.TimeField(verbose_name='Время посещения')
    count = models.IntegerField(verbose_name='Количество гостей')
    table = models.ForeignKey('Table', verbose_name='Столик', on_delete=models.DO_NOTHING)
    client = models.CharField(max_length=32, verbose_name='Гость', null=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    is_finishing = models.BooleanField(default=False, verbose_name='Завершено')

    def __str__(self):
        return 'Бронирование #' + str(self.pk) + ' | ' + self.phone

    def get_absolute_url(self):
        return reverse('reservation', kwargs={'reservation_id': self.pk})

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class ReservationHistory(models.Model):
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата посещения')
    reservation = models.ForeignKey('Reservation', verbose_name='Бронирование', on_delete=models.SET_NULL, null=True)
    total = models.FloatField(verbose_name='Общая стоимость чека')
    served = models.ForeignKey(User, verbose_name='Обслуживал(а)', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Посещение #' + str(self.pk) + ' | ' + self.reservation.phone

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'История посещений'


class Photo(models.Model):
    image = models.ImageField(verbose_name='Изображение')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return 'Фотография #' + str(self.pk)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Review(models.Model):
    author = models.CharField(max_length=128, verbose_name='Автор')
    reservation_history = models.ForeignKey('ReservationHistory', on_delete=models.CASCADE, verbose_name='Посещение')
    description = models.CharField(max_length=512, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оставления отзыва')

    def __str__(self):
        return 'Отзыв #' + str(self.pk) + ' от ' + self.author

    def get_absolute_url(self):
        return reverse('review', kwargs={'review_id': self.pk})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')
    name = models.CharField(max_length=64, verbose_name='Имя гостя')
    visit_date = models.DateField(verbose_name='Дата посещения')
    visit_time = models.TimeField(verbose_name='Время посещения')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    count = models.IntegerField(verbose_name='Количество гостей')
    archived = models.BooleanField(default=False, verbose_name='Обработано')

    def __str__(self):
        return self.phone + ' | ' + self.name

    def get_absolute_url(self):
        return reverse('request', kwargs={'request_id': self.pk})

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


User.add_to_class('__str__', lambda obj: f"{obj.first_name} {obj.last_name} [{obj.username}]")
