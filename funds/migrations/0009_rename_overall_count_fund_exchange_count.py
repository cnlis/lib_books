# Generated by Django 3.2.9 on 2021-12-05 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0008_auto_20211205_0852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fund',
            old_name='overall_count',
            new_name='exchange_count',
        ),
    ]