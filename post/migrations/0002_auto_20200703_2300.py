# Generated by Django 3.0.8 on 2020-07-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('USER', 'USER'), ('MODERATOR', 'MODERATOR'), ('ADMIN', 'ADMIN')], default='USER', max_length=12, unique=True),
        ),
    ]