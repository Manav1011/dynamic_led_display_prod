# Generated by Django 4.2.6 on 2024-03-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("serial_comm", "0009_alter_states_mean_alter_statesweekly_mean"),
    ]

    operations = [
        migrations.AlterField(
            model_name="states",
            name="mean",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="statesweekly",
            name="mean",
            field=models.CharField(max_length=255),
        ),
    ]
