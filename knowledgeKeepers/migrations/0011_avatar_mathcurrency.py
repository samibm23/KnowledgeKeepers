# Generated by Django 4.1.7 on 2023-05-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgeKeepers', '0010_avatar_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatar',
            name='mathcurrency',
            field=models.IntegerField(default=5),
        ),
    ]