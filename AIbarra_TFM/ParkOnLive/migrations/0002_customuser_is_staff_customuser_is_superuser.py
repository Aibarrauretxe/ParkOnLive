# Generated by Django 5.0.3 on 2024-03-12 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ParkOnLive", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]