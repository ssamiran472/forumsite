# Generated by Django 3.0.9 on 2020-09-06 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.CharField(default='slug', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.CharField(default='slug', max_length=200),
            preserve_default=False,
        ),
    ]