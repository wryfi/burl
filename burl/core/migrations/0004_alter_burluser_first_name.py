# Generated by Django 4.0.2 on 2022-02-24 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_migrate_redirects_briefurls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burluser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
