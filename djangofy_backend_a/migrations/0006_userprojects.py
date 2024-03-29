# Generated by Django 4.1.7 on 2023-05-11 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangofy_backend_a', '0005_alter_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_link', models.CharField(blank=True, max_length=100, null=True)),
                ('project_name', models.CharField(max_length=100)),
                ('project_data', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangofy_backend_a.user')),
            ],
        ),
    ]
