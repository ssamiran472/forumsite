# Generated by Django 3.0.9 on 2020-09-14 01:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_contactus_isread'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='submit_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]