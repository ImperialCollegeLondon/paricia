# Generated by Django 2.1.1 on 2019-02-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicion', '0006_auto_20190211_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caudal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='DireccionViento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='HumedadAire',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='HumedadSuelo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='NivelAgua',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='Precipitacion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion_id', models.PositiveIntegerField(verbose_name='estacion_id')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Valor')),
            ],
        ),
        migrations.CreateModel(
            name='PresionAtmosferica',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='RadiacionSolar',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='TemperaturaAgua',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='VelocidadViento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.CreateModel(
            name='Viento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('estacion', models.PositiveIntegerField(verbose_name='Estacion')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('vel_valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('vel_maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('vel_minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
                ('dir_valor', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Valor')),
                ('dir_maximo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Máximo')),
                ('dir_minimo', models.DecimalField(decimal_places=6, max_digits=14, null=True, verbose_name='Mínimo')),
            ],
        ),
        migrations.DeleteModel(
            name='Var1',
        ),
        migrations.DeleteModel(
            name='Var10',
        ),
        migrations.DeleteModel(
            name='Var11',
        ),
        migrations.DeleteModel(
            name='Var2',
        ),
        migrations.DeleteModel(
            name='Var3',
        ),
        migrations.DeleteModel(
            name='Var4',
        ),
        migrations.DeleteModel(
            name='Var5',
        ),
        migrations.DeleteModel(
            name='Var6',
        ),
        migrations.DeleteModel(
            name='Var7',
        ),
        migrations.DeleteModel(
            name='Var8',
        ),
        migrations.DeleteModel(
            name='Var9',
        ),
        migrations.AddIndex(
            model_name='viento',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_vi_estacio_bf1db5_idx'),
        ),
        migrations.AddIndex(
            model_name='viento',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_vi_fecha_6d74ae_idx'),
        ),
        migrations.AddIndex(
            model_name='velocidadviento',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_ve_estacio_b73ed3_idx'),
        ),
        migrations.AddIndex(
            model_name='velocidadviento',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_ve_fecha_023d1e_idx'),
        ),
        migrations.AddIndex(
            model_name='temperaturaagua',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_te_estacio_38ed0b_idx'),
        ),
        migrations.AddIndex(
            model_name='temperaturaagua',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_te_fecha_be0aa9_idx'),
        ),
        migrations.AddIndex(
            model_name='radiacionsolar',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_ra_estacio_a39f13_idx'),
        ),
        migrations.AddIndex(
            model_name='radiacionsolar',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_ra_fecha_ca81e4_idx'),
        ),
        migrations.AddIndex(
            model_name='presionatmosferica',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_pr_estacio_a202fe_idx'),
        ),
        migrations.AddIndex(
            model_name='presionatmosferica',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_pr_fecha_bb7ccf_idx'),
        ),
        migrations.AddIndex(
            model_name='precipitacion',
            index=models.Index(fields=['estacion_id', 'fecha'], name='medicion_pr_estacio_190a5b_idx'),
        ),
        migrations.AddIndex(
            model_name='precipitacion',
            index=models.Index(fields=['fecha', 'estacion_id'], name='medicion_pr_fecha_3b07e1_idx'),
        ),
        migrations.AddIndex(
            model_name='nivelagua',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_ni_estacio_159657_idx'),
        ),
        migrations.AddIndex(
            model_name='nivelagua',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_ni_fecha_1ae364_idx'),
        ),
        migrations.AddIndex(
            model_name='humedadsuelo',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_hu_estacio_fe4ec1_idx'),
        ),
        migrations.AddIndex(
            model_name='humedadsuelo',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_hu_fecha_a4b426_idx'),
        ),
        migrations.AddIndex(
            model_name='humedadaire',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_hu_estacio_ef9102_idx'),
        ),
        migrations.AddIndex(
            model_name='humedadaire',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_hu_fecha_032b2d_idx'),
        ),
        migrations.AddIndex(
            model_name='direccionviento',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_di_estacio_4544b6_idx'),
        ),
        migrations.AddIndex(
            model_name='direccionviento',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_di_fecha_615e05_idx'),
        ),
        migrations.AddIndex(
            model_name='caudal',
            index=models.Index(fields=['estacion', 'fecha'], name='medicion_ca_estacio_555616_idx'),
        ),
        migrations.AddIndex(
            model_name='caudal',
            index=models.Index(fields=['fecha', 'estacion'], name='medicion_ca_fecha_da2171_idx'),
        ),
    ]