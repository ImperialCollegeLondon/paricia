# Generated by Django 5.1 on 2024-09-05 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0006_alter_sensor_sensor_brand_alter_sensor_sensor_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Owner of the object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', help_text="Visibility level of the object. WARNING: Changing this setting will affect the permissions of the object. If 'Public', all users will be able to view and associate the object with their own.", max_length=8),
        ),
        migrations.AlterField(
            model_name='sensorbrand',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Owner of the object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sensorbrand',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', help_text="Visibility level of the object. WARNING: Changing this setting will affect the permissions of the object. If 'Public', all users will be able to view and associate the object with their own.", max_length=8),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Owner of the object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', help_text="Visibility level of the object. WARNING: Changing this setting will affect the permissions of the object. If 'Public', all users will be able to view and associate the object with their own.", max_length=8),
        ),
    ]
