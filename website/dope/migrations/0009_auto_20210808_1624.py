# Generated by Django 3.2.5 on 2021-08-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dope', '0008_auto_20210801_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['date'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
