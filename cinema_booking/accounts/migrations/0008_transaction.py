# Generated by Django 5.0.9 on 2024-11-27 19:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_card_card_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=255, unique=True)),
                ('masked_card', models.CharField(max_length=19)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['transaction_id'], name='accounts_tr_transac_d339cb_idx'), models.Index(fields=['customer'], name='accounts_tr_custome_ef0346_idx'), models.Index(fields=['created_at'], name='accounts_tr_created_b2c597_idx')],
            },
        ),
    ]
