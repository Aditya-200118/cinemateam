# Generated by Django 5.0.9 on 2024-11-09 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_promotion_description_promotion_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='valid_to',
            field=models.DateField(default=datetime.date(2024, 12, 9)),
        ),
    ]