# Generated by Django 4.1.7 on 2023-05-28 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_participant_score_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='parent_id',
            field=models.IntegerField(default=-1),
        ),
    ]