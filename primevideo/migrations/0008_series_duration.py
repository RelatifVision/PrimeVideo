# Generated by Django 5.1.1 on 2024-11-10 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primevideo', '0007_alter_series_options_series_watched'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
