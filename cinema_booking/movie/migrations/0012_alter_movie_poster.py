# Generated by Django 5.0.9 on 2024-11-09 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_showroom_seat_count_delete_seat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='movie/posters'),
        ),
    ]
