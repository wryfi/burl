# Generated by Django 2.0.3 on 2018-04-02 03:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('redirects', '0002_auto_20180401_1710'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='URL',
            new_name='Redirect',
        ),
    ]
