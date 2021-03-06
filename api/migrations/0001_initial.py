# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 02:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_type', models.CharField(max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('search', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=20)),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Credit')),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Precipitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=-1.0, max_digits=5)),
                ('min_value', models.DecimalField(decimal_places=2, default=-1.0, max_digits=5)),
                ('max_value', models.DecimalField(decimal_places=2, default=-1.0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Pressure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=10)),
                ('value', models.DecimalField(decimal_places=2, default=-1.0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Sun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rise', models.DateTimeField()),
                ('set', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=245)),
                ('number', models.IntegerField()),
                ('var', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=10)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('period', models.IntegerField(blank=True, null=True)),
                ('forecast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Forecast')),
                ('precipitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Precipitation')),
                ('pressure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Pressure')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Symbol')),
                ('temperature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Temperature')),
            ],
            options={
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='TimeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=255)),
                ('utcoffsetMinutes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WindDirection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.DecimalField(decimal_places=2, default=-1.0, max_digits=5)),
                ('name', models.CharField(max_length=245)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WindSpeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mps', models.DecimalField(decimal_places=2, default=-1.0, max_digits=5)),
                ('name', models.CharField(max_length=245)),
            ],
        ),
        migrations.AddField(
            model_name='time',
            name='wind_direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WindDirection'),
        ),
        migrations.AddField(
            model_name='time',
            name='wind_speed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WindSpeed'),
        ),
        migrations.AddField(
            model_name='location',
            name='timezone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TimeZone'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Location'),
        ),
        migrations.AddField(
            model_name='forecast',
            name='sun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sun'),
        ),
    ]
