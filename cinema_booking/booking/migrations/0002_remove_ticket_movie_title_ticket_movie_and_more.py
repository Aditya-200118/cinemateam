# Generated by Django 5.0.9 on 2024-10-29 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
        ('movie', '0006_movie_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='movie_title',
        ),
        migrations.AddField(
            model_name='ticket',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.movie'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
