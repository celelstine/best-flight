# Generated by Django 2.2.2 on 2019-06-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bestflightApp', '0002_airlineflightpath_airline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airlineflightpath',
            options={'verbose_name_plural': 'Airplane Flight Paths'},
        ),
        migrations.AlterModelOptions(
            name='airplanecapacity',
            options={'verbose_name_plural': 'Airplane Capacities'},
        ),
        migrations.AlterModelOptions(
            name='availableflight',
            options={'verbose_name_plural': 'Available Flights'},
        ),
        migrations.AlterModelOptions(
            name='flightclass',
            options={'ordering': ('title',), 'verbose_name_plural': 'Flight Classes'},
        ),
        migrations.AlterField(
            model_name='airlineflightpath',
            name='date_last_flight',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
