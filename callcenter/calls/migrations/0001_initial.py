# Generated by Django 4.0.1 on 2022-01-25 05:22

from django.db import migrations, models
import django.db.models.deletion
import tkinter.tix


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(help_text='Введите адрес', max_length=100, null=tkinter.tix.Tree)),
                ('number', models.CharField(help_text='Введите номер дома', max_length=10, null=tkinter.tix.Tree)),
                ('building', models.CharField(help_text='Введите номер строения', max_length=10, null=tkinter.tix.Tree)),
                ('room', models.CharField(help_text='Введите номер квартиры', max_length=10, null=tkinter.tix.Tree)),
            ],
        ),
        migrations.CreateModel(
            name='Call_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите значение', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название города или поселка', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите сокращенное название МО', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Manipulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите вид консультации', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите ФИО пациента', max_length=400)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите причину обращения', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите подпричину обращения', max_length=200)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calls.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('call_number', models.CharField(help_text='Введите номер с которого звонили', max_length=11)),
                ('callback_number', models.CharField(help_text='Введите номер с которого для обратной связи', max_length=11)),
                ('question', models.TextField()),
                ('registration_covid_date', models.DateField(null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.address')),
                ('call_result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.call_result')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.city')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.hospital')),
                ('manipulation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.manipulation')),
                ('patient', models.ManyToManyField(to='calls.Patient')),
                ('sub_subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.sub_subject')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.subject')),
            ],
        ),
    ]
