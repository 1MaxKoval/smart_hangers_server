# Generated by Django 3.2.5 on 2021-10-25 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hangers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendarentry',
            options={'ordering': ['date_time']},
        ),
    ]