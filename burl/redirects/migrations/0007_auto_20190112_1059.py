# Generated by Django 2.0.5 on 2019-01-12 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0006_auto_20180521_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='random',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='burl',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Brief URL'),
        ),
    ]
