# Generated by Django 5.1 on 2024-08-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0003_remove_dataimporttemp_format_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataimport',
            name='log',
            field=models.TextField(default='', help_text='Log of the data ingestion, indicating any errors', verbose_name='Data ingestion log'),
        ),
        migrations.AddField(
            model_name='dataimport',
            name='reprocess',
            field=models.BooleanField(default=False, help_text='If checked, the data will be reprocessed', verbose_name='Reprocess data'),
        ),
        migrations.AddField(
            model_name='dataimport',
            name='status',
            field=models.TextField(choices=[('N', 'Not queued'), ('Q', 'Queued'), ('C', 'Completed'), ('F', 'Failed')], default='N', help_text='Status of the import', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='dataimport',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='dataimport',
            name='records',
            field=models.IntegerField(blank=True, null=True, verbose_name='Records'),
        ),
        migrations.AlterField(
            model_name='dataimport',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start date'),
        ),
    ]