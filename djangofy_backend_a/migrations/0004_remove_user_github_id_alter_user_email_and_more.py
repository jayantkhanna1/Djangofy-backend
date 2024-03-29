# Generated by Django 4.1.7 on 2023-05-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangofy_backend_a', '0003_user_github_id_alter_user_email_alter_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='github_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
