# Generated by Django 4.0.1 on 2022-01-27 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0005_rename_name_patient_patient_fio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
