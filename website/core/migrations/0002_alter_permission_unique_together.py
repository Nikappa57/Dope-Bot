# Generated by Django 3.2.5 on 2021-08-18 18:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dope', '0013_auto_20210818_1822'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('user', 'gateway')},
        ),
    ]
