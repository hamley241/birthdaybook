# Generated by Django 2.2.6 on 2019-10-16 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birthdays', '0002_auto_20191016_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='bday',
            new_name='birthday',
        ),
    ]