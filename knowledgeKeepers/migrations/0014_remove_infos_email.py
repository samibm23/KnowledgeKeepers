# Generated by Django 3.2.18 on 2023-05-11 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgeKeepers', '0013_mathproblemhistory_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infos',
            name='email',
        ),
    ]