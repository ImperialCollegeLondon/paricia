# Generated by Django 4.2.7 on 2024-02-22 06:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("measurement", "0008_report_completeness"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="measurement",
            name="used_for_hourly",
        ),
        migrations.RemoveField(
            model_name="report",
            name="used_for_daily",
        ),
        migrations.RemoveField(
            model_name="report",
            name="used_for_monthly",
        ),
    ]
