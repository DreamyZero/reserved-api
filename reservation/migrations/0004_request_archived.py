# Generated by Django 4.1.3 on 2023-03-23 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_review_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Обработано'),
        ),
    ]
