# Generated by Django 3.2.9 on 2021-12-05 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0005_auto_20211205_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='type',
        ),
        migrations.RemoveField(
            model_name='exchange',
            name='is_income',
        ),
    ]
