# Generated by Django 4.2.11 on 2025-01-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("xauth", "0008_remove_student_parents_student_parents"),
    ]

    operations = [
        migrations.AddField(
            model_name="degree",
            name="completion_period",
            field=models.PositiveIntegerField(default=4),
        ),
    ]
