# Generated by Django 3.0.8 on 2020-07-03 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_auto_20200703_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subreddit',
            name='moderators',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
