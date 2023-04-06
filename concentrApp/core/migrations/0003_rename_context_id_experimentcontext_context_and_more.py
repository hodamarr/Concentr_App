# Generated by Django 4.1.7 on 2023-04-06 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_context_experiment_experimentcontext_participant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experimentcontext',
            old_name='context_id',
            new_name='context',
        ),
        migrations.RenameField(
            model_name='experimentcontext',
            old_name='experiment_id',
            new_name='experiment',
        ),
        migrations.RenameField(
            model_name='participantsubmission',
            old_name='experiment_context_id',
            new_name='experiment_context',
        ),
        migrations.RenameField(
            model_name='participantsubmission',
            old_name='participant_id',
            new_name='participant',
        ),
        migrations.RenameField(
            model_name='participantsubmissionanswer',
            old_name='participant_submission_id',
            new_name='participant_submission',
        ),
    ]
