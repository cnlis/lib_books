# Generated by Django 3.2.9 on 2021-12-05 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0012_fund_order_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='comment',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='comment',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
