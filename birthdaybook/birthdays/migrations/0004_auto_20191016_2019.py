# Generated by Django 2.2.6 on 2019-10-16 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthdays', '0003_auto_20191016_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='birthday',
            field=models.DateField(),
        ),
    ]
