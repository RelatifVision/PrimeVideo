# Generated by Django 5.1.1 on 2024-10-17 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_tasks_datecompleted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('content_type', models.CharField(choices=[('MOVIE', 'Película'), ('SERIES', 'Serie')], max_length=6)),
                ('status', models.CharField(choices=[('UNWATCHED', 'No visto'), ('WATCHING', 'Viendo'), ('COMPLETED', 'Completado')], default='UNWATCHED', max_length=10)),
                ('favorite', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
