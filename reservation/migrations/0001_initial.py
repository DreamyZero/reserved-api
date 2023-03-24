# Generated by Django 4.1.2 on 2022-11-12 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Название')),
                ('description', models.CharField(max_length=64, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.CharField(blank=True, max_length=128, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('name', models.CharField(max_length=64, verbose_name='Имя гостя')),
                ('visit_date', models.DateField(verbose_name='Дата посещения')),
                ('visit_time', models.TimeField(verbose_name='Время посещения')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('count', models.IntegerField(verbose_name='Количество гостей')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('visit_date', models.DateField(verbose_name='Дата посещения')),
                ('visit_time', models.TimeField(verbose_name='Время посещения')),
                ('count', models.IntegerField(verbose_name='Количество гостей')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('is_finishing', models.BooleanField(default=False, verbose_name='Завершено')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.CreateModel(
            name='ReservationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата посещения')),
                ('total', models.FloatField(verbose_name='Общая стоимость чека')),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.reservation', verbose_name='Бронирование')),
                ('served', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Обслуживал(а)')),
            ],
            options={
                'verbose_name': 'Посещение',
                'verbose_name_plural': 'История посещений',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256, verbose_name='Описание')),
                ('capacity', models.IntegerField(verbose_name='Вместимость')),
                ('is_reserved', models.BooleanField(default=False, verbose_name='Зарезервирован/Занят')),
                ('category', models.ManyToManyField(to='reservation.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Столик',
                'verbose_name_plural': 'Столики',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128, verbose_name='Автор')),
                ('description', models.CharField(max_length=512, verbose_name='Описание')),
                ('reservation_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.reservationhistory', verbose_name='Посещение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reservation.table', verbose_name='Столик'),
        ),
    ]