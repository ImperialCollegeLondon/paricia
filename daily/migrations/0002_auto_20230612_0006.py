# Generated by Django 3.2.14 on 2023-06-12 00:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("daily", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="airtemperature",
            name="date",
        ),
        migrations.RemoveField(
            model_name="atmosphericpressure",
            name="date",
        ),
        migrations.RemoveField(
            model_name="batteryvoltage",
            name="date",
        ),
        migrations.RemoveField(
            model_name="chlorineconcentrationdepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="flow",
            name="date",
        ),
        migrations.RemoveField(
            model_name="flowmanual",
            name="date",
        ),
        migrations.RemoveField(
            model_name="humidity",
            name="date",
        ),
        migrations.RemoveField(
            model_name="indirectradiation",
            name="date",
        ),
        migrations.RemoveField(
            model_name="oxygenconcentrationdepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="percentageoxygenconcentrationdepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="phycocyanindepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="precipitation",
            name="date",
        ),
        migrations.RemoveField(
            model_name="redoxpotentialdepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="soilmoisture",
            name="date",
        ),
        migrations.RemoveField(
            model_name="soiltemperature",
            name="date",
        ),
        migrations.RemoveField(
            model_name="solarradiation",
            name="date",
        ),
        migrations.RemoveField(
            model_name="striplevelreading",
            name="date",
        ),
        migrations.RemoveField(
            model_name="wateraciditydepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="waterlevel",
            name="date",
        ),
        migrations.RemoveField(
            model_name="watertemperature",
            name="date",
        ),
        migrations.RemoveField(
            model_name="watertemperaturedepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="waterturbiditydepth",
            name="date",
        ),
        migrations.RemoveField(
            model_name="winddirection",
            name="date",
        ),
        migrations.RemoveField(
            model_name="windvelocity",
            name="date",
        ),
        migrations.AlterField(
            model_name="airtemperature",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="atmosphericpressure",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="batteryvoltage",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="chlorineconcentrationdepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="flow",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="flowmanual",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="humidity",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="indirectradiation",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="oxygenconcentrationdepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="percentageoxygenconcentrationdepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="phycocyanindepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="precipitation",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="redoxpotentialdepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="soilmoisture",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="soiltemperature",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="solarradiation",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="striplevelreading",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="wateraciditydepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="waterlevel",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="watertemperature",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="watertemperaturedepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="waterturbiditydepth",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="winddirection",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
        migrations.AlterField(
            model_name="windvelocity",
            name="time",
            field=models.DateField(verbose_name="time"),
        ),
    ]