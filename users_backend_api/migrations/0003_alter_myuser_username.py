# Generated by Django 4.1.3 on 2022-12-08 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_backend_api', '0002_alter_otpmodel_creation_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='Username'),
        ),
    ]