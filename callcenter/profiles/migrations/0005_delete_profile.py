# Generated by Django 4.0.1 on 2022-02-08 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]