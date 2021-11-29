# Generated by Django 3.2.9 on 2021-11-28 06:52

import books.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=14, unique=True)),
                ('author', models.TextField(max_length=300)),
                ('title', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=14, unique=True)),
                ('title', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_from', models.IntegerField(default=1)),
                ('class_to', models.IntegerField(default=1)),
                ('suffix', models.CharField(blank=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='русский язык', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='неизвестно', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='неизвестно', max_length=20)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='-', max_length=50, unique=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='source',
            constraint=models.UniqueConstraint(fields=('title', 'date'), name='unique_source'),
        ),
        migrations.AddConstraint(
            model_name='klass',
            constraint=models.UniqueConstraint(fields=('class_from', 'class_to', 'suffix'), name='unique_class'),
        ),
        migrations.AddField(
            model_name='book',
            name='classes',
            field=models.ForeignKey(default=books.models.blank_class, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='books.klass'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(default=books.models.blank_language, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='books.language'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(default=books.models.blank_publisher, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='books.publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='source',
            field=models.ForeignKey(default=books.models.blank_source, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='books.source'),
        ),
        migrations.AddField(
            model_name='book',
            name='special',
            field=models.ForeignKey(default=books.models.blank_special, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='books.special'),
        ),
    ]
