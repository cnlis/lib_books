# Generated by Django 3.2.9 on 2021-12-05 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0011_fund_income_count_ex'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='order_count',
            field=models.IntegerField(default=0),
        ),
    ]
