# Generated by Django 4.1.3 on 2022-11-30 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="issue", name="assignee",),
    ]
