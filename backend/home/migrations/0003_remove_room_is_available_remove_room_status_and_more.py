# Generated by Django 5.1.3 on 2024-12-24 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_customer_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='room',
            name='status',
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
