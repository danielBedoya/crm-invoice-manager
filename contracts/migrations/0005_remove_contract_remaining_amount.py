# Generated by Django 4.2.20 on 2025-05-15 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_contract_remaining_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='remaining_amount',
        ),
    ]
