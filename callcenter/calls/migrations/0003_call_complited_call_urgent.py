# Generated by Django 4.0.1 on 2022-01-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_alter_call_registration_covid_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='complited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='call',
            name='urgent',
            field=models.BooleanField(default=False),
        ),
    ]
