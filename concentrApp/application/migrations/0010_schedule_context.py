# Generated by Django 4.1.7 on 2023-06-07 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_question_related_answer_alter_experiment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='context',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='application.context'),
        ),
    ]