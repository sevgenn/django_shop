# Generated by Django 3.1 on 2020-08-29 15:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20200828_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='sex',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 31, 18, 10, 34, 523408)),
        ),
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='tags')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='about me')),
                ('gender', models.CharField(blank=True, choices=[('male', 'М'), ('female', 'Ж')], max_length=6, verbose_name='sex')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]