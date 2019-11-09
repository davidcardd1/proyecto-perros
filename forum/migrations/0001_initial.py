# Generated by Django 2.2.7 on 2019-11-08 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, default='', upload_to='', verbose_name='Profile pic')),
                ('post_count', models.IntegerField(blank=True, default=0, verbose_name='Post count')),
                ('bio', models.TextField(blank=True, default='', max_length=2500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Subject')),
                ('description', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated')),
                ('no_views', models.IntegerField(blank=True, default=0, verbose_name='Views count')),
                ('post_count', models.IntegerField(blank=True, default=0, verbose_name='Post count')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='topics', to='forum.Usuario')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicUser', to='forum.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('post_count', models.IntegerField(blank=True, default=0, verbose_name='Post count')),
                ('topic', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forum.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forum.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('thread', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.Usuario')),
            ],
        ),
    ]
