# Generated by Django 3.0.9 on 2020-09-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200907_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='fullName',
            field=models.CharField(default='English', max_length=30),
            preserve_default=False,
        ),
    ]
