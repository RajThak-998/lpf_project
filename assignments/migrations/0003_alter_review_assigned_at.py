# Generated by Django 5.1.3 on 2024-12-23 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_review_assigned_at_alter_review_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='assigned_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]