# Generated by Django 4.2.16 on 2024-11-25 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomments',
            name='content',
            field=models.CharField(max_length=257),
        ),
    ]