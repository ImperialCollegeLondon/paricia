# Generated by Django 3.2.14 on 2023-06-18 00:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hourly", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="airtemperature",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="airtemperature",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="atmosphericpressure",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="atmosphericpressure",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="batteryvoltage",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="batteryvoltage",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="chlorineconcentrationdepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="chlorineconcentrationdepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="flow",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="flow",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="humidity",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="humidity",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="indirectradiation",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="indirectradiation",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="oxygenconcentrationdepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="oxygenconcentrationdepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="percentageoxygenconcentrationdepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="percentageoxygenconcentrationdepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="phycocyanindepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="phycocyanindepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="redoxpotentialdepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="redoxpotentialdepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="soilmoisture",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="soilmoisture",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="soiltemperature",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="soiltemperature",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="solarradiation",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="solarradiation",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="wateraciditydepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="wateraciditydepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="waterlevel",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="waterlevel",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="watertemperature",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="watertemperature",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="watertemperaturedepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="watertemperaturedepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="waterturbiditydepth",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="waterturbiditydepth",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="winddirection",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="winddirection",
            name="minimum",
        ),
        migrations.RemoveField(
            model_name="windvelocity",
            name="maximum",
        ),
        migrations.RemoveField(
            model_name="windvelocity",
            name="minimum",
        ),
    ]