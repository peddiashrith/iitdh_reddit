# Generated by Django 3.0.8 on 2020-07-03 17:29

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('USER', 'USER'), ('MODERATOR', 'MODERATOR'), ('ADMIN', 'ADMIN')], default='USER', max_length=12, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='SubReddit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='post.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.Role')),
                ('subreddit_following', models.ManyToManyField(to='post.SubReddit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=256)),
                ('links', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True, max_length=500, null=True), size=10)),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('PENDING', 'PENDING'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subreddit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.SubReddit')),
                ('tags', models.ManyToManyField(to='post.Tag')),
            ],
        ),
    ]
