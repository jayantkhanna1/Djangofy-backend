# Generated by Django 4.1.7 on 2023-05-10 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangofy_backend_a', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='private_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='type_of_user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
