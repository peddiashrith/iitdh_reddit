# Generated by Django 3.0.8 on 2020-07-03 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20200703_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='post.Tag'),
        ),
    ]