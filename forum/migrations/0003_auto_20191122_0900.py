# Generated by Django 2.2.7 on 2019-11-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20191121_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(max_length=5000, verbose_name='Message'),
        ),
    ]
