# Generated by Django 5.0.9 on 2024-12-11 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0028_alter_promotion_valid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='valid_to',
            field=models.DateField(default=datetime.date(2025, 1, 10)),
        ),
    ]