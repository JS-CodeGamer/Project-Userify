# Generated by Django 4.1.3 on 2022-12-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_backend_api', '0005_alter_myuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
