# Generated by Django 3.2.14 on 2023-06-21 01:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("daily", "0004_auto_20230618_0016"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="precipitation",
            name="total",
        ),
        migrations.AddField(
            model_name="precipitation",
            name="sum",
            field=models.DecimalField(
                decimal_places=2, max_digits=6, null=True, verbose_name="Sum"
            ),
        ),
    ]