# Generated by Django 3.2.9 on 2021-12-09 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0014_auto_20211209_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='funds.income'),
        ),
    ]