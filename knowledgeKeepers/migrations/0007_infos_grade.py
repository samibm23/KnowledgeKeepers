# Generated by Django 4.1.7 on 2023-05-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgeKeepers', '0006_infos_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='infos',
            name='grade',
            field=models.TextField(blank=True, null=True),
        ),
    ]
