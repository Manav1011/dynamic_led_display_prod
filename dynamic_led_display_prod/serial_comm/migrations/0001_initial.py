# Generated by Django 4.2.6 on 2023-10-18 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RS232',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RTC', models.CharField(max_length=255)),
                ('AvgeSpeed', models.CharField(max_length=255)),
                ('AvgeTemp', models.CharField(max_length=255)),
                ('AvgeHum', models.CharField(max_length=255)),
                ('AvgeSr', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RS485',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RTC', models.CharField(max_length=255)),
                ('AvgeSpeed', models.CharField(max_length=255)),
                ('AvgeTemp', models.CharField(max_length=255)),
                ('AvgeHum', models.CharField(max_length=255)),
                ('AvgeSr', models.CharField(max_length=255)),
            ],
        ),
    ]