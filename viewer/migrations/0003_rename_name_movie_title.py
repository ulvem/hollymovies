# Generated by Django 4.0.4 on 2022-06-03 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_movie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='name',
            new_name='title',
        ),
    ]
