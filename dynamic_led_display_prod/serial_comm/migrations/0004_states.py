# Generated by Django 4.2.6 on 2023-11-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("serial_comm", "0003_alter_serialcommunication_atmp_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="States",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("param", models.CharField(max_length=255)),
                ("count", models.IntegerField()),
                ("mean", models.FloatField()),
                ("min", models.FloatField()),
                ("max", models.FloatField()),
                ("std", models.FloatField()),
            ],
        ),
    ]
