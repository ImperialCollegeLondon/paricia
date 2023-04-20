from variable.models import Variable
# from estacion.models import Estacion
from django.apps import apps
import pandas as pd
import numpy as np
from django.db.models import IntegerField, Value, BooleanField
# from diario.models import Var2Diario
import decimal as dec
from datetime import datetime, timedelta, time


# def reporte_diario(station, variable, start_time, end_time, maximum, minimum):
def daily_validation(station, variable, start_time, end_time, minimum, maximum):
    reporte, series = daily_report_dataframes(station, variable, start_time, end_time, minimum, maximum)
    # reporte, series = calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum)
    reporte.rename(
        columns={
            'date':'fecha',
            'date_error':'fecha_error',
            # 'repeated_values_count':'fecha_numero',
            'extra_data_count': 'fecha_numero',
            'avg_value':'valor',
            'max_maximum':'maximo',
            'min_minimum':'minimo',
            'data_existence_percentage':'porcentaje',
            'is_null':'porcentaje_error',
            'value_error':'valor_error',
            'maximum_error':'maximo_error',
            'minimum_error':'minimo_error',
            'suspicious_values_count':'valor_numero',
            'suspicious_maximums_count':'maximo_numero',
            'suspicious_minimums_count':'minimo_numero',
            'historic_diary_avg':'media_historica',
            'state':'estado',
            'all_validated':'validado',
            'value_difference_error_count':'c_varia_err',
        },
        inplace=True
    )


    # response = acumulado.to_dict(orient='list')
    # response = _records.to_dict(orient='records')
    if variable.variable_id in [4, 5]:
        reporte['n_valor'] = 0
    else:
        reporte['n_valor'] = reporte['c_varia_err']
    num_fecha = len(reporte[reporte['fecha_error'].ne(1) & ~reporte['fecha_error'].isna()].index)
    num_porcentaje = len(reporte[reporte['porcentaje_error'].eq(True)])
    num_valor = len(reporte[reporte['porcentaje_error'].eq(False) & ~reporte['valor_numero'].isna()])
    num_maximo = len(reporte[reporte['porcentaje_error'].eq(False) & ~reporte['maximo_numero'].isna()])
    num_minimo = len(reporte[reporte['porcentaje_error'].eq(False) & ~reporte['minimo_numero'].isna()])
    num_dias = len(reporte.index)

    data = {'estacion': [{
        'est_id': station.station_id,
        'est_nombre': station.station_name,
        }],
        'variable': [{
            'var_id': variable.variable_id,
            'var_nombre': variable.name,
            'var_maximo': variable.maximum,
            'var_minimo': variable.minimum,
            'var_unidad_sigla': variable.unit.initials,
            'es_acumulada': variable.is_cumulative,
        }],
        'datos': reporte.fillna('').to_dict(orient='records'),
        'indicadores': [{
            'num_fecha': num_fecha,
            'num_porcentaje': num_porcentaje,
            'num_valor': num_valor,
            'num_maximo': num_maximo,
            'num_minimo': num_minimo,
            'num_dias': num_dias
        }],
        'datos_grafico': series.fillna('').values.tolist(),#datos_grafico,
        'grafico': None,#grafico_msj,
        'curva': None,#mensaje
    }
    return data


# Basic calculations is the main functions for calculations
def basic_calculations(station, variable, start_time, end_time, inf_lim_variable, sup_lim_variable):
    # TODO change tx_period for the code to query from model
    tx_period = 5
    Measurement = apps.get_model(app_label='measurement', model_name=variable.variable_code)
    Validated = apps.get_model(app_label='validated', model_name=variable.variable_code)

    validated = Validated.objects.filter(
        station_id=station.station_id,
        time__gte=start_time,
        time__lte=end_time
    ).annotate(
        # is_validated: True is for 'validated' tables, False for raw 'measurement'
        is_validated=Value(True, output_field=BooleanField()),
        exists_in_validated=Value(True, output_field=BooleanField()),
        null_value=Value(False, output_field=BooleanField())
    ).order_by('time')

    value_fields = ('value', 'minimum', 'maximum')
    base_fields = ('id', 'time', 'is_validated', 'exists_in_validated', 'null_value')
    fields = base_fields + value_fields
    validated = pd.DataFrame.from_records(
        validated.values(*fields)
    )

    if validated.empty:
        validated = pd.DataFrame(columns=fields)

    # TODO WHich one is faster?
    # # validated['time'] = validated['time'].dt.floor('min')
    # validated['time'] = validated['time'].values.astype('<M8[m]')
    # TODO for testing: time_truncated
    validated['time_truncated'] = validated['time'].values.astype('<M8[m]')
    # validated['date'] = pd.to_datetime(validated['time']).dt.date

    measurement = Measurement.objects.filter(
        station_id=station.station_id,
        time__gte=start_time,
        time__lte=end_time
    ).annotate(
        # is_validated: True is for 'validated' tables, False for raw 'measurement'
        is_validated=Value(False, output_field=BooleanField()),
    ).order_by('time')

    value_fields = ('value', 'minimum', 'maximum')
    base_fields = ('id', 'time', 'is_validated')
    fields = base_fields + value_fields
    measurement = pd.DataFrame.from_records(
        measurement.values(*fields)
    )

    if measurement.empty:
        measurement = pd.DataFrame(columns=fields)

    measurement['time_truncated'] = measurement['time'].values.astype('<M8[m]')
    # measurement['date'] = pd.to_datetime(measurement['time']).dt.date

    # TODO analizar eliminacion campos 'null_value' : parece ser innecesario o fácilmente eliminable
    # measurement['null_value'] = measurement['time_truncated'].isin(validated['time_truncated'])
    # TODO Probabliy is not necessary to math 'time' and 'value'
    # matches_time_and_value = pd.merge(measurement, validated, on=['time_truncated', 'value'], how='outer', indicator=True)

    # TODO IMPORTANT: Verify all of matches_time and 'exists_in_validated' computations
    matches_time = pd.merge(measurement, validated, on=['time_truncated'], how='outer', indicator=True)
    # TODO Specially, Check the following line: It´s not doing the right thing.
    measurement['exists_in_validated'] = matches_time['_merge'] == 'both'

    joined = pd.concat([validated, measurement]).sort_values(by=['time_truncated', 'is_validated', 'id'], ascending=[True, False, False])
    joined['date'] = pd.to_datetime(measurement['time']).dt.date
    joined.rename(columns={'id': 'db_row_id'}, inplace=True)
    joined.reset_index(drop=True, inplace=True)

    joined.index.name = 'id_joined'
    joined.reset_index(inplace=True)
    # joined.reset_index(names='id_joined', inplace=True)

    inf_lim_variable = float(inf_lim_variable)
    sup_lim_variable = float(sup_lim_variable)
    joined['suspicious_value'] = ~joined['value'].between(inf_lim_variable, sup_lim_variable)
    joined['suspicious_maximum'] = ~joined['maximum'].between(inf_lim_variable, sup_lim_variable)
    joined['suspicious_minimum'] = ~joined['minimum'].between(inf_lim_variable, sup_lim_variable)

    # selected
    # TODO check if 'is_selected' is used in later
    selected = joined.drop_duplicates('time_truncated', keep='first')
    selected.reset_index(drop=True, inplace=True)
    selected['is_selected'] = True
    joined = joined.merge(selected[['id_joined', 'is_selected']], on='id_joined', how='left', indicator=False)
    joined['is_selected'].fillna(False, inplace=True)

    # Moved from original to reuse code
    # TODO Ask if using 'time_truncated' is better option
    selected['time_lapse'] = selected['time_truncated'] - selected['time_truncated'].shift(1)
    selected['time_lapse'] = selected['time_lapse'].dt.total_seconds()/60
    selected['time_lapse_status'] = selected['time_lapse'].apply(
        lambda x: 0 if x < tx_period else (1 if x == tx_period else 2)
        # TODO check again, in validation_report too
        # When is 2 or 3
    )
    selected['time_lapse_status'][0] = 1

    selected['lagged_value'] = np.where(
        selected['time_lapse_status'].le(1),
        selected['value'].shift(1),
        np.nan,
    )

    joined = joined.merge(selected[['time_truncated', 'time_lapse_status', 'lagged_value']],
                          on='time_truncated',
                          how='left',
                          indicator=False)
    joined['value_difference'] = joined['value'] - joined['lagged_value']
    # TODO implement to a error/warning level (variable.diff_error and variable.diff_warning)
    joined['value_difference_error'] = np.where(
        joined['value_difference'].abs().gt(variable.diff_error),
        True,  # Error
        False,  # No Error
    )
    # # Basic statistics
    # mean = selected['value'].mean(skipna=True)
    # std_dev = selected['value'].astype(float).std(skipna=True)
    # stddev_inf_limit = mean - (std_dev * float(variable.var_min))
    # stddev_sup_limit = mean + (std_dev * float(variable.var_min))
    return measurement, validated, joined, selected, tx_period





# def calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum):
# def reporte_diario_dataframes(station, variable, start_time, end_time, minimum, maximum):
def daily_report_dataframes(station, variable, start_time, end_time, minimum, maximum):

    measurement, validated, joined, selected, tx_period = basic_calculations(station, variable, start_time, end_time, minimum, maximum)

    # TODO: implement all for
    daily_group_all = joined.groupby('date')

    # REF. NAME: tabla_acumulada
    # daily calculations
    daily_group = selected.groupby('date')
    daily = daily_group['date'].count()
    daily = daily.reset_index(name='data_count')
    # daily['date'] = pd.to_datetime(daily['date']).dt.date
    # TODO Ask if those aggregation functions must be calculated over 'selected' table instead of 'joined'
    daily['avg_value'] = daily_group['value'].mean().to_numpy()
    daily['max_maximum'] = daily_group['maximum'].max().to_numpy()
    daily['min_minimum'] = daily_group['minimum'].min().to_numpy()
    daily['all_validated'] = daily_group['is_validated'].all().to_numpy()

    # REF. NAME: tabla_datos_esperados
    # Expected data count for each day. Uses "period"
    # TODO Create a "period" table for storing the period for every station
    # TODO Maybe program for dynamic periods. This happens when a station change the period

    expected_data_count = 24 * 60 / tx_period

    # REF. NAME: tabla_calculo
    # Percentage of data existence
    daily['data_existence_percentage'] = (daily['data_count'] / expected_data_count ) * 100.0
    # TODO escoger la correcta para PARICIA
    daily['is_null'] = daily['data_existence_percentage'] < (100.0 - float(variable.null_limit))
    # daily['is_null'] = daily['data_existence_percentage'] < variable.null_limit


    # REF. NAME: tabla_valores_sos
    # Count of suspicious values:  values over variable.maximum or under variable.minimum
    # TODO: change variable_maximun and variable_minimum to apply for PARICIA context
    # variable.var_minimo -> variable.minimum
    # variable.var_maximo -> variable.maximum

    # daily['suspicious_values_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='value',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily['suspicious_values_count'] = daily_group['suspicious_value'].count()
    # daily['suspicious_maximums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='maximum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily['suspicious_maximums_count'] = daily_group['suspicious_maximum'].count()
    # daily['suspicious_minimums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='minimum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily['suspicious_minimums_count'] = daily_group['suspicious_minimum'].count()

    # TODO check this for PARAMH2O (tabla_varia_erro)
    # REF. NAME: tabla_varia_erro
    # Calculating consecutive differences and check for errors.
    # 'time_lapse_status' set to:
    #                               0 if 'time_lapse' < 'period'
    #                               1 if 'time_lapse' == 'period'
    #                               2 if 'time_lapse' > 'period'
    #

    # TODO Check what would be the best option
    # daily['value_difference_error_count'] = daily_group['value_difference_error'].sum(numeric_only=False).to_numpy()
    daily['value_difference_error_count'] = daily_group_all['value_difference_error'].sum(numeric_only=False).to_numpy()


    # # REF. NAME: lapsos_dias
    # # Generate a sequence of days following in the calendar to compare with data in database and note voids
    # # TODO Analizar que esto pudiera ser incluído en la primera generación de daily
    # calendar_day_seq = pd.DataFrame(
    #     pd.date_range(start=start_time, end=end_time).date,
    #     columns=['date']
    # )
    # daily = calendar_day_seq.merge(daily, on='date', how='left')

    if daily.empty:
        daily = df = pd.DataFrame(columns=['id', 'date', 'data_count', 'avg_value', 'max_maximum', 'min_minimum',
            'all_validated', 'data_existence_percentage', 'is_null',
            'suspicious_values_count', 'suspicious_maximums_count',
            'suspicious_minimums_count', 'value_difference_error_count',
            'day_interval', 'date_error', 'extra_data_count', 'historic_diary_avg',
            'state', 'value_error', 'maximum_error', 'minimum_error']
                                  )
        return daily, selected[['time', 'value']]

    # REF. NAME: fecha_error o dia_error
    daily['day_interval'] = (daily['date'] - daily['date'].shift(1)).dt.days
    daily['day_interval'][0] = 1
    daily['date_error'] = np.where(daily['day_interval'].gt(1), 3, 1)
    # TODO hacer un groupby de repeated_values_count por día, para pasar el valor total de repetidos por día
    #      posiblemente convenga hacer un solo cálculo arriba

    # fecha_numero: repeated_values_count
    # # REF. NAME: tabla_duplicados
    # # count_of_repeated
    repeated_in_validated = validated.groupby(['time_truncated'])['time_truncated'].count()
    repeated_in_validated = repeated_in_validated.reset_index(name="repeated_in_validated")
    repeated_in_validated['repeated_in_validated'] = np.where(
        repeated_in_validated['repeated_in_validated'].gt(0),
        repeated_in_validated['repeated_in_validated'] - 1,
        0,
    )

    repeated_in_measurement = measurement.groupby(['time_truncated'])['time_truncated'].count()
    repeated_in_measurement = repeated_in_measurement.reset_index(name="repeated_in_measurement")
    repeated_in_measurement['repeated_in_measurement'] = np.where(
        repeated_in_measurement['repeated_in_measurement'].gt(0),
        repeated_in_measurement['repeated_in_measurement'] - 1,
        0,
    )
    extra_data_count = pd.merge(repeated_in_validated,
                          repeated_in_measurement,
                          on=['time_truncated'],
                          how='outer',
                          indicator=False)
    extra_data_count.fillna(0, inplace=True)
    extra_data_count.sort_values(by=['time_truncated'], inplace=True)
    extra_data_count['extra_values_count'] = extra_data_count['repeated_in_validated'] + \
                                             extra_data_count['repeated_in_measurement']
    extra_data_count['date'] = pd.to_datetime(extra_data_count['time_truncated']).dt.date

    extra_data_daily_group = extra_data_count[extra_data_count['extra_values_count'] > 0].groupby('date')
    extra_data_daily = extra_data_daily_group['extra_values_count'].sum()
    extra_data_daily = extra_data_daily.reset_index(name='extra_data_count')
    daily = daily.merge(extra_data_daily, on='date', how='left')
    daily['extra_data_count'].fillna(0, inplace=True)

    # porcentaje : data_existence_percentage
    # porcentaje_error : null_value
    # valor_error : (posiblemente no requiera)
    # maximo_error : (posiblemente no requiera)
    # minimo_error : (posiblemente no requiera)
    # valor_numero : suspicious_values_count
    # maximo_numero : suspicious_maximums_count
    # minimo_numero : suspicious_minimums_count
    # media_historica : historic_mean
    # SELECT AVG(dp.valor) FROM diario_var2diario dp WHERE dp.estacion_id = 4 AND
    # date_part('day',dp.fecha)= 13 AND date_part('month',dp.fecha)= 10
    # historic_diaries = Var2Diario.objects.filter(estacion_id=station.est_id, fecha__day=)


    month_day_tuples = tuple(list(zip(
        pd.DatetimeIndex(daily['date']).month,
        pd.DatetimeIndex(daily['date']).day
    )))
    Daily = apps.get_model(app_label='daily', model_name=variable.variable_code)
    historic_diary = Daily.objects.filter(station_id=station.station_id).extra(
        where=["(date_part('month', date), date_part('day', date)) in %s"],
        params=[month_day_tuples]
    )
    historic_diary = pd.DataFrame(list(historic_diary.values()))
    if not historic_diary.empty:
        historic_diary['month-day'] = pd.DatetimeIndex(historic_diary['date']).month.astype(str) \
                                      + '-' + pd.DatetimeIndex(historic_diary['date']).day.astype(str)
        historic_diary_group = historic_diary.groupby(['month-day'])
        daily['historic_diary_avg'] = historic_diary_group['value'].mean().to_numpy()
    else:
        daily['historic_diary_avg'] = np.nan



    # estado : state
    daily['state'] = True

    # validado :

    # validated_only = selected[['date', 'is_validated']].loc[selected['is_validated'] == True]
    # validated_count = validated_only.groupby('date')['date'].count().reset_index(name='validated_count')
    # daily = daily.merge(validated_count, on='date', how='left')
    # daily['validated_count'].fillna(0, inplace=True)

    # daily['all_validated'] = daily_group['is_validated'].all().to_numpy()

    # c_varia_err

    daily['data_count'].fillna(0, inplace=True)
    daily['data_existence_percentage'].fillna(0, inplace=True)
    daily['suspicious_values_count'].fillna(0, inplace=True)
    daily['suspicious_maximums_count'].fillna(0, inplace=True)
    daily['suspicious_minimums_count'].fillna(0, inplace=True)
    daily['value_difference_error_count'].fillna(0, inplace=True)
    daily['historic_diary_avg'].fillna('', inplace=True)

    ##
    # TODO check, maybe it's not needed anymore
    daily['value_error'] = np.where(daily['suspicious_values_count'].gt(0), True, False,)
    daily['maximum_error'] = np.where(daily['suspicious_maximums_count'].gt(0), True, False, )
    daily['minimum_error'] = np.where(daily['suspicious_minimums_count'].gt(0), True, False, )
    #
    ##

    # Round decimals
    # TODO cambiar 'valor' por 'value' en pAricia
    Measurement = apps.get_model(app_label='measurement', model_name=variable.variable_code)
    decimal_places = Measurement._meta.get_field('value').decimal_places
    daily['avg_value'] = daily['avg_value'].astype(np.float64).round(decimal_places)
    daily['max_maximum'] = daily['max_maximum'].astype(np.float64).round(decimal_places)
    daily['min_minimum'] = daily['min_minimum'].astype(np.float64).round(decimal_places)
    daily['data_existence_percentage'] = daily['data_existence_percentage'].astype(np.float64).round(1)

    # daily.reset_index(names='id', inplace=True)
    daily.index.name = 'id'
    daily.reset_index(inplace=True)
    ## TODO Eliminar o corregir ids -> id
    #
    # daily.rename(columns={'id':'ids',}, inplace=True)
    daily['ids'] = daily['id']
    #
    ##
    return daily, selected[['time', 'value']]



def calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum):
    # variable_id = 2
    # station_id = 4
    # start_time = '2022-10-11 00:00:00'
    # end_time = '2022-10-25 23:59:59'

    # Period (or "frecuency") number of minutes between every captured data (e.g. 5 minutes, 10 minutes)
    tx_period = 5


    model_name = 'Var' + str(variable.var_id)
    Measurement = apps.get_model(app_label='medicion', model_name=model_name+'Medicion')
    Validated = apps.get_model(app_label='validacion', model_name=model_name+'Validado')

    #
    variable = Variable.objects.get(pk=variable.var_id)
    station = Estacion.objects.get(pk=station.est_id)

    # filter_args = {}
    # validated = pd.DataFrame.from_records(validated.values(**filter_args))
    validated = Validated.objects.filter(
        estacion_id=station.est_id,
        fecha__gte=start_time,
        fecha__lte=end_time
    ).annotate(
        is_validated=Value(True, output_field=BooleanField()),# True is for 'validated' tables, False for raw 'measurement'
        exists_in_validated=Value(True, output_field=BooleanField()),
        null_value=Value(False, output_field=BooleanField())
    ).order_by('fecha')
    validated = pd.DataFrame.from_records(
        validated.values('id', 'fecha', 'is_validated', 'valor', 'maximo', 'minimo', 'exists_in_validated', 'null_value')
    )
    # TODO: eliminar
    validated = validated.rename(columns={'fecha':'time',  'valor':'value', 'maximo':'maximum', 'minimo':'minimum'})
    if validated.empty:
        validated = pd.DataFrame(columns=['id', 'time', 'is_validated', 'value', 'maximum', 'minimum',
                                          'exists_in_validated', 'null_value'])

    # TODO WHich one is faster?
    # # validated['time'] = validated['time'].dt.floor('min')
    # validated['time'] = validated['time'].values.astype('<M8[m]')
    # TODO for testing: time_truncated

    validated['time_truncated'] = validated['time'].values.astype('<M8[m]')


    # validated['date'] = pd.to_datetime(validated['time']).dt.date


    measurement = Measurement.objects.filter(
        estacion_id=station.est_id,
        fecha__gte=start_time,
        fecha__lte=end_time
    ).annotate(
        is_validated=Value(False, output_field=BooleanField()),# True is for 'validated' tables, False for raw 'measurement'
    ).order_by('fecha')
    measurement = pd.DataFrame.from_records(
        measurement.values('id', 'fecha', 'is_validated', 'valor', 'maximo', 'minimo')
    )
    # TODO eliminar
    measurement = measurement.rename(columns={'fecha':'time', 'valor':'value', 'maximo':'maximum', 'minimo':'minimum'})
    if measurement.empty:
        measurement = pd.DataFrame(columns=['id', 'time', 'is_validated', 'value', 'maximum', 'minimum',
                                          'exists_in_validated', 'null_value'])

    # measurement['time'] = measurement['time'].values.astype('<M8[m]')
    measurement['time_truncated'] = measurement['time'].values.astype('<M8[m]')
    # measurement['date'] = pd.to_datetime(measurement['time']).dt.date

    # TODO analizar eliminacion campos 'null_value' : parece ser innecesario o fácilmente eliminable
    # measurement['null_value'] = measurement['time_truncated'].isin(validated['time_truncated'])
    # TODO Probabliy is not necessary to math 'time' and 'value'
    # matches_time_and_value = pd.merge(measurement, validated, on=['time_truncated', 'value'], how='outer', indicator=True)
    matches_time = pd.merge(measurement, validated, on=['time_truncated'], how='outer', indicator=True)
    measurement['exists_in_validated'] = matches_time['_merge'] == 'both'


    joined = pd.concat([validated, measurement]).sort_values(by=['time_truncated', 'is_validated', 'id'], ascending=[True, False, False])
    joined['date'] = pd.to_datetime(measurement['time']).dt.date
    joined.rename(columns={'id': 'db_row_id'}, inplace=True)
    joined.reset_index(drop=True, inplace=True)
    joined.reset_index(names='id_joined', inplace=True)


    # # REF. NAME: tabla_duplicados
    # # count_of_repeated
    repeated_in_validated = validated.groupby(['time_truncated'])['time_truncated'].count()
    repeated_in_validated = repeated_in_validated.reset_index(name="repeated_in_validated")
    repeated_in_validated['repeated_in_validated'] = np.where(
        repeated_in_validated['repeated_in_validated'].gt(0),
        repeated_in_validated['repeated_in_validated'] - 1,
        0,
    )

    repeated_in_measurement = measurement.groupby(['time_truncated'])['time_truncated'].count()
    repeated_in_measurement = repeated_in_measurement.reset_index(name="repeated_in_measurement")
    repeated_in_measurement['repeated_in_measurement'] = np.where(
        repeated_in_measurement['repeated_in_measurement'].gt(0),
        repeated_in_measurement['repeated_in_measurement'] - 1,
        0,
    )
    extra_data_count = pd.merge(repeated_in_validated,
                          repeated_in_measurement,
                          on=['time_truncated'],
                          how='outer',
                          indicator=False)
    extra_data_count.fillna(0, inplace=True)
    extra_data_count.sort_values(by=['time_truncated'], inplace=True)
    extra_data_count['extra_values_count'] = extra_data_count['repeated_in_validated'] + \
                                             extra_data_count['repeated_in_measurement']
    extra_data_count['date'] = pd.to_datetime(extra_data_count['time_truncated']).dt.date

    # joined = joined.merge(
    #     extra_data_count[['time_truncated', 'extra_values_count']],
    #     on='time_truncated',
    #     how='left',
    #     indicator=False)


    # selected
    # TODO check if 'is_selected' is used in later
    selected = joined.drop_duplicates('time_truncated', keep='first')
    selected.reset_index(drop=True, inplace=True)
    selected['is_selected'] = True
    joined = joined.merge(selected[['id_joined', 'is_selected']], on='id_joined', how='left', indicator=False)
    joined['is_selected'].fillna(False, inplace=True)


    # Moved from original to reuse code
    # TODO Ask if using 'time_truncated' is better option
    selected['time_lapse'] = selected['time_truncated'] - selected['time_truncated'].shift(1)
    selected['time_lapse'] = selected['time_lapse'].dt.total_seconds()/60
    selected['time_lapse_status'] = selected['time_lapse'].apply(
        lambda x: 0 if x < tx_period else (1 if x == tx_period else 2)
    )
    selected['time_lapse_status'][0] = 1
    #
    # joined = joined.merge(selected[['time_truncated', 'time_lapse_status']], on='time_truncated', how='left', indicator=False)
    #

    # TODO It could be value difference of not selected also. Ask
    selected['value_difference'] = np.where(
        selected['time_lapse_status'].eq(1),
        selected['value'] - selected['value'].shift(1),
        np.nan,
    )
    selected['value_difference_error'] = np.where(
        selected['value_difference'].abs().gt(variable.var_err),
        True,# Error
        False,# No Error
    )




    # REF. NAME: tabla_acumulada
    # daily calculations
    daily_group = selected.groupby('date')
    daily = daily_group['date'].count()
    daily = daily.reset_index(name='data_count')
    # daily['date'] = pd.to_datetime(daily['date']).dt.date
    # TODO Ask if those aggregation functions must be calculated over 'selected' table instead of 'joined'
    daily['avg_value'] = daily_group['value'].mean().to_numpy()
    daily['max_maximum'] = daily_group['maximum'].max().to_numpy()
    daily['min_minimum'] = daily_group['minimum'].min().to_numpy()
    daily['all_validated'] = daily_group['is_validated'].all().to_numpy()

    # REF. NAME: tabla_datos_esperados
    # Expected data count for each day. Uses "period"
    # TODO Create a "period" table for storing the period for every station
    # TODO Maybe program for dynamic periods. This happens when a station change the period

    expected_data_count = 24 * 60 / tx_period

    # REF. NAME: tabla_calculo
    # Percentage of data existence
    daily['data_existence_percentage'] = (daily['data_count'] / expected_data_count ) * 100.0
    # TODO escoger la correcta para PARICIA
    # daily['is_null'] = daily['data_existence_percentage'] < variable.null_limit
    daily['is_null'] = daily['data_existence_percentage'] < variable.umbral_completo

    # REF. NAME: tabla_valores_sos
    # Count of suspicious values:  values over variable.maximum or under variable.minimum
    # TODO: change variable_maximun and variable_minimum to apply for PARICIA context
    # variable.var_minimo -> variable.minimum
    # variable.var_maximo -> variable.maximum

    daily['suspicious_values_count'] = daily_group.agg(
        suspicious=pd.NamedAgg(
            column='value',
            aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
        )).to_numpy()
    daily['suspicious_maximums_count'] = daily_group.agg(
        suspicious=pd.NamedAgg(
            column='maximum',
            aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
        )).to_numpy()
    daily['suspicious_minimums_count'] = daily_group.agg(
        suspicious=pd.NamedAgg(
            column='minimum',
            aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
        )).to_numpy()

    # TODO check this for PARAMH2O (tabla_varia_erro)
    # REF. NAME: tabla_varia_erro
    # Calculating consecutive differences and check for errors.
    # 'time_lapse_status' set to:
    #                               0 if 'time_lapse' < 'period'
    #                               1 if 'time_lapse' == 'period'
    #                               2 if 'time_lapse' > 'period'
    #

    daily['value_difference_error_count'] = daily_group['value_difference_error'].sum(numeric_only=False).to_numpy()


    # # REF. NAME: lapsos_dias
    # # Generate a sequence of days following in the calendar to compare with data in database and note voids
    # # TODO Analizar que esto pudiera ser incluído en la primera generación de daily
    # calendar_day_seq = pd.DataFrame(
    #     pd.date_range(start=start_time, end=end_time).date,
    #     columns=['date']
    # )
    # daily = calendar_day_seq.merge(daily, on='date', how='left')

    if daily.empty:
        daily = df = pd.DataFrame(columns=['id', 'date', 'data_count', 'avg_value', 'max_maximum', 'min_minimum',
            'all_validated', 'data_existence_percentage', 'is_null',
            'suspicious_values_count', 'suspicious_maximums_count',
            'suspicious_minimums_count', 'value_difference_error_count',
            'day_interval', 'date_error', 'extra_data_count', 'historic_diary_avg',
            'state', 'value_error', 'maximum_error', 'minimum_error']
                                  )
        return daily, selected[['time', 'value']]

    # REF. NAME: fecha_error o dia_error
    daily['day_interval'] = (daily['date'] - daily['date'].shift(1)).dt.days
    daily['day_interval'][0] = 1
    daily['date_error'] = np.where(daily['day_interval'].gt(1), 3, 1)
    # TODO hacer un groupby de repeated_values_count por día, para pasar el valor total de repetidos por día
    #      posiblemente convenga hacer un solo cálculo arriba

    # fecha_numero: repeated_values_count
    extra_data_daily_group = extra_data_count[extra_data_count['extra_values_count'] > 0].groupby('date')
    extra_data_daily = extra_data_daily_group['extra_values_count'].sum()
    extra_data_daily = extra_data_daily.reset_index(name='extra_data_count')
    daily = daily.merge(extra_data_daily, on='date', how='left')
    daily['extra_data_count'].fillna(0, inplace=True)

    # porcentaje : data_existence_percentage
    # porcentaje_error : null_value
    # valor_error : (posiblemente no requiera)
    # maximo_error : (posiblemente no requiera)
    # minimo_error : (posiblemente no requiera)
    # valor_numero : suspicious_values_count
    # maximo_numero : suspicious_maximums_count
    # minimo_numero : suspicious_minimums_count
    # media_historica : historic_mean
    # SELECT AVG(dp.valor) FROM diario_var2diario dp WHERE dp.estacion_id = 4 AND
    # date_part('day',dp.fecha)= 13 AND date_part('month',dp.fecha)= 10
    # historic_diaries = Var2Diario.objects.filter(estacion_id=station.est_id, fecha__day=)


    month_day_tuples = tuple(list(zip(
        pd.DatetimeIndex(daily['date']).month,
        pd.DatetimeIndex(daily['date']).day
    )))
    historic_diary = Var2Diario.objects.filter(estacion_id=station.est_id).extra(
        where=["(date_part('month', fecha), date_part('day', fecha)) in %s"],
        params=[month_day_tuples]
    )
    historic_diary = pd.DataFrame(list(historic_diary.values()))
    historic_diary = historic_diary.rename(columns={'fecha':'date',  'valor':'value'})
    historic_diary['month-day'] = pd.DatetimeIndex(historic_diary['date']).month.astype(str) \
                                  + '-' + pd.DatetimeIndex(historic_diary['date']).day.astype(str)
    historic_diary_group = historic_diary.groupby(['month-day'])
    daily['historic_diary_avg'] = historic_diary_group['value'].mean().to_numpy()


    # estado : state
    daily['state'] = True

    # validado :

    # validated_only = selected[['date', 'is_validated']].loc[selected['is_validated'] == True]
    # validated_count = validated_only.groupby('date')['date'].count().reset_index(name='validated_count')
    # daily = daily.merge(validated_count, on='date', how='left')
    # daily['validated_count'].fillna(0, inplace=True)

    # daily['all_validated'] = daily_group['is_validated'].all().to_numpy()

    # c_varia_err

    daily['data_count'].fillna(0, inplace=True)
    daily['data_existence_percentage'].fillna(0, inplace=True)
    daily['suspicious_values_count'].fillna(0, inplace=True)
    daily['suspicious_maximums_count'].fillna(0, inplace=True)
    daily['suspicious_minimums_count'].fillna(0, inplace=True)
    daily['value_difference_error_count'].fillna(0, inplace=True)


    ##
    # TODO check, maybe it's not needed anymore
    daily['value_error'] = np.where(daily['suspicious_values_count'].gt(0), True, False,)
    daily['maximum_error'] = np.where(daily['suspicious_maximums_count'].gt(0), True, False, )
    daily['minimum_error'] = np.where(daily['suspicious_minimums_count'].gt(0), True, False, )
    #
    ##

    # Round decimals
    # TODO cambiar 'valor' por 'value' en pAricia
    decimal_places = Measurement._meta.get_field('valor').decimal_places
    daily['avg_value'] = daily['avg_value'].astype(np.float64).round(decimal_places)
    daily['max_maximum'] = daily['max_maximum'].astype(np.float64).round(decimal_places)
    daily['min_minimum'] = daily['min_minimum'].astype(np.float64).round(decimal_places)
    daily['data_existence_percentage'] = daily['data_existence_percentage'].astype(np.float64).round(1)
    daily.reset_index(names='id', inplace=True)
    ## TODO Eliminar o corregir ids -> id
    #
    # daily.rename(columns={'id':'ids',}, inplace=True)
    daily['ids'] = daily['id']
    #
    ##
    return daily, selected[['time', 'value']]


# Consultar datos crudos y/o validados por estacion, variable y fecha de un día en específico
def detalle_diario(est_id, var_id, fecha_str, sup_lim_variable, inf_lim_variable):
    # SQL fun : reporte_validacion_modelo
    # SQL template: validacion_crudos_prom.sql

    start_time = datetime.strptime(fecha_str, '%Y-%m-%d')
    end_time = datetime.combine(start_time.date(), time(23, 59, 59, 999999))
    variable = Variable.objects.get(var_id=var_id)
    # period = 5


    measurement, validated, joined, selected, tx_period = basic_calculations(est_id, var_id, start_time, end_time, tx_period)



    joined['state'] = ~(joined['value'].isna() & joined['maximum'].isna() & joined['minimum'].isna())
    # Basic statistics
    mean = selected['value'].mean(skipna=True)
    std_dev = selected['value'].astype(float).std(skipna=True)
    stddev_inf_limit = mean - (std_dev * float(variable.var_min))
    stddev_sup_limit = mean + (std_dev * float(variable.var_min))
    joined['stddev_error'] = ~joined['value'].between(stddev_inf_limit, stddev_sup_limit)
    joined['comment'] = ''

    joined.fillna('', inplace=True)

    report = joined[['id_joined', 'time', 'value', 'maximum', 'minimum', 'is_validated', 'is_selected', 'state',
                     'time_lapse_status', 'value_error', 'maximum_error', 'minimum_error', 'stddev_error', 'comment',
                     'value_difference', 'value_difference_error']]
    report.rename(columns={'id_joined': 'id'}, inplace=True)
    #######
    joined['n_valor'] = joined['value_difference']
    _selected = joined[joined['is_selected']==True]
    num_fecha = len(_selected[_selected['time_lapse_status'] != 1].index)

    # Only take into account 'value_error' when there's no error in timestamp lapse
    _selected_NO_TIMELAPSE_ERROR = _selected[_selected['time_lapse_status'] == 1]
    num_valor = len(_selected_NO_TIMELAPSE_ERROR[_selected_NO_TIMELAPSE_ERROR['value_error'] == True].index)
    num_maximo = len(_selected[_selected['maximum_error'] == True].index)
    num_minimo = len(_selected[_selected['minimum_error'] == True].index)
    num_stddev = len(_selected[_selected['stddev_error'] == True].index)


    # TODO check if this es expected number of data
    num_datos = int(24 * (60/tx_period))

    report.rename(
        columns={
            # 'id': '',
            'time': 'fecha',
            'value': 'valor',
            'maximum': 'maximo',
            'minimum': 'minimo',
            'is_validated': 'validado',
            'is_selected': 'seleccionado',
            'state': 'estado',
            'time_lapse_status': 'fecha_error',
            'value_error': 'valor_error',
            'maximum_error': 'maximo_error',
            'minimum_error': 'minimo_error',
            'stddev_error': 'stddev_error',
            'comment': 'comentario',
            'value_difference': 'variacion_consecutiva',
            'value_difference_error': 'varia_error'
        },
        inplace=True
    )


    data = {
        'datos': report.to_dict(orient='records'),
        'indicadores': [{
            'num_fecha': num_fecha,
            'num_valor': num_valor,
            'num_valor1':num_valor,
            'num_maximo': num_maximo,
            'num_minimo': num_minimo,
            'num_stddev': num_stddev,
            'num_datos': num_datos
        }]
    }

    return data


def get_condiciones(cambios_lista):
    fechas_condicion = []
    fechas_eliminar = []
    for fila in cambios_lista:
        if fila['validado']:
            fechas_condicion.append("'" + fila['fecha'] + "'")
        if not fila['estado']:
            fechas_eliminar.append("'" + fila['fecha'] + "'")

    fechas_condicion = set(fechas_condicion)
    fechas_eliminar = set(fechas_eliminar)

    where_fechas = ",".join(fechas_condicion)
    where_eliminar = ",".join(fechas_eliminar)

    condiciones = {
        'where_eliminar': where_eliminar,
        'where_fechas': where_fechas
    }
    return condiciones


# Pasar los datos crudos a validados
def pasar_crudos_validados(cambios_lista, variable, estacion_id, condiciones, limite_superior, limite_inferior):
    model_name = 'Var' + str(variable.var_id)
    Measurement = apps.get_model(app_label='medicion', model_name=model_name+'Medicion')
    Validated = apps.get_model(app_label='validacion', model_name=model_name+'Validado')
    # modelo = normalize(variable.var_nombre).replace(" de ", "")
    # modelo = modelo.replace(" ", "")
    variable_nombre = variable.var_codigo
    fecha_inicio_dato = cambios_lista[0]['fecha']
    fecha_fin_dato = cambios_lista[-1]['fecha']
    # where_fechas = condiciones.get('where_fechas')
    where_eliminar = condiciones.get('where_eliminar')

    #
    reporte_recibido = pd.DataFrame.from_records(cambios_lista)
    #

    if variable.var_id == 1:
        query = "select * FROM reporte_crudos_precipitacion(%s, %s, %s, %s, %s);"

    elif variable.var_id == 4 or variable.var_id == 5:
        query = "select * FROM reporte_crudos_viento(%s, %s, %s, %s, %s);"
    else:
        query = "select * FROM reporte_crudos_" + variable.var_modelo.lower() + "(%s, %s, %s, %s, %s);"
    consulta = ReporteCrudos.objects.raw(query,
                                         [estacion_id, fecha_inicio_dato, fecha_fin_dato, limite_superior,
                                          limite_inferior])
    for fila in consulta:
        delattr(fila, '_state')

    datos = [dict(fila.__dict__) for fila in consulta]
    data_json = json.dumps(datos, cls=DjangoJSONEncoder)
    with connection.cursor() as cursor:
        if variable.var_id == 4 or variable.var_id == 5:
            cursor.callproc('insertar_viento_validacion', [estacion_id, data_json])
        #elif variable.var_id == 10 or variable.var_id == 11:
        #    cursor.callproc('insertar_agua_validacion', [estacion_id, data_json])
        else:
            print(data_json)
            print(estacion_id)
            cursor.callproc('insertar_' + variable.var_modelo.lower() + '_validacion', [estacion_id, data_json])
        resultado = cursor.fetchone()[0]
        cursor.close()

    if len(where_eliminar) > 0:
        if variable.var_id == 4 or variable.var_id == 5:
            variable_nombre = 'viento'
        #elif variable.var_id == 10 or variable.var_id == 11:
        #    variable_nombre = 'agua'

        if variable.var_id == 1:
            sql = """UPDATE validacion_var%%modelo%%validado SET valor = NULL WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%) """
        elif variable.var_id == 4 or variable.var_id == 5:
            sql = """UPDATE validacion_viento SET valor = NULL, maximo = NULL, minimo = NULL,         
                    direccion = null, categoria = null WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);
                    UPDATE validacion_var4validado SET valor = NULL, maximo = NULL, minimo = NULL        
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);
                    UPDATE validacion_var5validado SET valor = NULL, maximo = NULL, minimo = NULL
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%);"""
        #elif variable.var_id == 10 or variable.var_id == 11:
        #    sql = """UPDATE validacion_var%%modelo%%validado SET nivel = NULL, caudal = NULL
        #            WHERE estacion_id = %%est_id%% AND date_trunc('day',fecha) IN (%%condicion%%)"""
        else:
            sql = """UPDATE validacion_var%%modelo%%validado SET valor = NULL, maximo = NULL, minimo = NULL 
                    WHERE estacion_id = %%est_id%%   
                    AND date_trunc('day',fecha) IN (%%condicion%%)"""

        sql_modificar = sql.replace("%%modelo%%", str(variable.var_id)).replace("%%est_id%%", str(estacion_id)) \
            .replace("%%condicion%%", where_eliminar)
        print(sql_modificar)
        with connection.cursor() as cursor:
            cursor.execute(sql_modificar)
            cursor.close()

    return resultado


def guardar_cambios_validacion (estacion_id, variable, tipo_transaccion, fecha_inicio, fecha_fin):
    sincronizacion = Sincronizacion(
        estacion_id=estacion_id,
        variable=variable,
        tipo_transaccion=tipo_transaccion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    sincronizacion.save()

"""    

"""






"""

CREATE OR REPLACE FUNCTION public.reporte_validacion_%%modelo%%(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone,  valor numeric,maximo numeric, minimo numeric,
    validado boolean, seleccionado boolean, estado boolean, fecha_error numeric, valor_error boolean,
    maximo_error boolean, minimo_error boolean, stddev_error boolean, comentario character varying
    , variacion_consecutiva numeric, varia_error boolean)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$
BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = 4),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 2),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.maximo, v.minimo, TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_var2validado v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= '2022-10-13 00:00:00' AND v.fecha <= '2022-10-13 23:59:59'
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, CASE WHEN m.valor = 'NaN' THEN NULL ELSE m.valor END,
        CASE WHEN m.maximo = 'NaN' THEN NULL ELSE m.maximo END,
        CASE WHEN m.minimo = 'NaN' THEN NULL ELSE m.minimo END,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha  AND v.valor IS NULL) AS valor_vacio
        FROM medicion_var2medicion m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= '2022-10-13 00:00:00' AND m.fecha <= '2022-10-13 23:59:59'
    ),
    --unir las tablas medicion y validacion
	union_med_val AS (
		SELECT * FROM validacion UNION SELECT * FROM medicion
	),
	--revision de lapsos de tiempo entre fechas
	lapsos_fechas AS (
		SELECT
			ff.fecha,
			row_number() OVER (ORDER BY ff.fecha ASC) as fecha_grupo,
			EXTRACT(EPOCH FROM ff.fecha - lag(ff.fecha) OVER (ORDER BY ff.fecha ASC))/60  as lapso_tiempo,
			(SELECT fre.fre_valor FROM frecuencia_frecuencia fre
					WHERE fre.var_id_id = (SELECT var_id FROM variable) AND fre.est_id_id = (SELECT est_id FROM estacion) AND fre.fre_fecha_ini < ff.fecha
					ORDER BY fre.fre_fecha_ini DESC LIMIT 1) AS periodo_esperado
		FROM (SELECT DISTINCT(umv.fecha) FROM union_med_val umv) ff ORDER BY fecha ASC
	),
	fechas AS (
		SELECT *,
			CASE WHEN fecha_grupo = 1 THEN 1 ELSE
			CASE WHEN lapso_tiempo < periodo_esperado - 0.13 THEN 0
				 WHEN lapso_tiempo > periodo_esperado + 0.13 THEN 3
				 WHEN lapso_tiempo = 0 THEN 0
				 WHEN LEAD(lapso_tiempo) OVER (ORDER by lf.fecha) > periodo_esperado + 0.13 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM lapsos_fechas lf
	),
	tabla_base AS (
		SELECT
			row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, --umv.validacion DESC--
			umv.id DESC) as numero_fila,
			*
		FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1 OR umv.valor_vacio = TRUE)
	),
	-- Excluir los datos duplicados
	tabla_seleccion AS (
		SELECT *,
			(SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE ELSE FALSE END END AS seleccionado
			--(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
		FROM tabla_base tb --WHERE tb.valor IS NOT NULL
	),
	tabla_variacion AS (
		SELECT *,
			(SELECT t1.valor - (SELECT tanterior.valor FROM tabla_seleccion tanterior
								WHERE tanterior.fecha_grupo = t1.fecha_grupo - 1
								AND tanterior.seleccionado IS TRUE) ) AS variacion_consecutiva,
			CASE WHEN t1.seleccionado THEN t1.valor ELSE NULL END AS valor_seleccionado
		FROM tabla_seleccion t1
	),
	estadistica AS (
		SELECT e1.media AS media, e1.desv_est AS desv_est,
		e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
		e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
		FROM (
			SELECT AVG(ts.valor) AS media, STDDEV_SAMP(ts.valor) AS desv_est
			FROM tabla_seleccion ts
			WHERE ts.valor IS NOT NULL AND ts.seleccionado IS TRUE
		) e1
	),
	reporte AS (
		SELECT ts.numero_fila AS id, ts.fecha, ts.valor, ts.maximo, ts.minimo, ts.existe_en_validacion, ts.seleccionado,
		    CASE WHEN ts.valor is NULL AND ts.maximo is NULL and ts.maximo is NULL THEN FALSE ELSE TRUE END as estado,
			(SELECT fecha_valida FROM fechas ff WHERE ff.fecha = ts.fecha)::numeric AS fecha_error,
			ts.valor > 29 OR ts.valor < 2 AS valor_error,
			ts.maximo > 29 OR ts.maximo < 2 AS maximo_error,
			ts.minimo > 29 OR ts.minimo < 2 AS minimo_error,
			ts.valor < (SELECT lim_inf_stddev FROM estadistica ) OR ts.valor > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
			CASE
				WHEN ts.existe_en_validacion THEN
					(SELECT vc.comentario FROM validacion_comentariovalidacion vc WHERE vc.estacion_id = (SELECT est_id FROM estacion) AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = ts.id)
				ELSE NULL
			END AS comentario,
			ts.variacion_consecutiva as variacion_consecutiva,
			ts.variacion_consecutiva <= -(select var_err from variable where var_id = 2) as varia_error
		FROM tabla_variacion ts
	)

	SELECT * FROM reporte;


END;
$BODY$;






















--- PARAMH2O
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = 4),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 2),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.maximo, v.minimo, TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_var2validado v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= '2022-10-13 00:00:00' AND v.fecha <= '2022-10-16 23:59:59'

    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, CASE WHEN m.valor = 'NaN' THEN NULL ELSE m.valor END,
        CASE WHEN m.maximo = 'NaN' THEN NULL ELSE m.maximo END,
        CASE WHEN m.minimo = 'NaN' THEN NULL ELSE m.minimo END,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha ) AS valor_vacio
        FROM medicion_var2medicion m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= '2022-10-13 00:00:00' AND m.fecha <= '2022-10-16 23:59:59'
    ),
    --unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
    lapsos_fechas AS (
		SELECT
			ff.fecha,
			row_number() OVER (ORDER BY ff.fecha ASC) as fecha_grupo,
			EXTRACT(EPOCH FROM ff.fecha - lag(ff.fecha) OVER (ORDER BY ff.fecha ASC))/60  as lapso_tiempo,
			(SELECT fre.fre_valor FROM frecuencia_frecuencia fre
					WHERE fre.var_id_id = (SELECT var_id FROM variable) AND fre.est_id_id = (SELECT est_id FROM estacion) AND fre.fre_fecha_ini < ff.fecha
					ORDER BY fre.fre_fecha_ini DESC LIMIT 1) AS periodo_esperado
		FROM (SELECT DISTINCT(umv.fecha) FROM union_med_val umv) ff ORDER BY fecha ASC
	),
	fechas AS (
		SELECT *,
			CASE WHEN fecha_grupo = 1 THEN 1 ELSE
			CASE WHEN lapso_tiempo < periodo_esperado - 0.13 THEN 0
				 WHEN lapso_tiempo > periodo_esperado + 0.13 THEN 3
				 WHEN lapso_tiempo = 0 THEN 0
				 WHEN LEAD(lapso_tiempo) OVER (ORDER by lf.fecha) > periodo_esperado + 0.13 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM lapsos_fechas lf
	),
    --Seleccionar una serie unica de los validados y los crudos
    tabla_base AS (
        SELECT
            row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.id DESC) as numero_fila,
            *
        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1 OR umv.valor_vacio = TRUE)
    ),
    tabla_seleccion AS (
		SELECT *,
			(SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE
		WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE
		ELSE FALSE END END AS seleccionado
			--(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
		FROM tabla_base tb --WHERE tb.valor IS NOT NULL
	),
	tabla_variacion AS (
		SELECT *,
			(SELECT t1.valor - (SELECT tanterior.valor FROM tabla_seleccion tanterior
								WHERE tanterior.fecha_grupo = t1.fecha_grupo - 1
								AND tanterior.seleccionado IS TRUE) ) AS variacion_consecutiva,
			CASE WHEN t1.seleccionado THEN t1.valor ELSE NULL END AS valor_seleccionado
		FROM tabla_seleccion t1
	),
    -- valores duplicados por cada fecha
    tabla_duplicados AS (

        SELECT tb.fecha, date_trunc('day',tb.fecha) as dia, COUNT(*) AS num_duplicados
        FROM tabla_base tb
        GROUP BY tb.fecha
        HAVING COUNT(*) > 1
        ORDER BY tb.fecha
    ),
    -- acumular los datos a diario
    tabla_acumulada AS (
        SELECT date_trunc('day',tb.fecha) as dia, COUNT(tb.valor) numero_datos,
        AVG(tb.valor) as valor, MAX(tb.maximo) as maximo, MIN(tb.minimo) as minimo,
        bool_and(tb.existe_en_validacion) as existe_en_validacion
        FROM tabla_base tb GROUP BY dia ORDER by dia
    ),
    -- Numero de datos esperados por d?a
    tabla_datos_esperados AS (
        SELECT ta.dia, ta.numero_datos,
        (SELECT CAST(1440/f.fre_valor AS INT) ndatos FROM frecuencia_frecuencia f WHERE f.fre_valor <= 60
            and f.est_id_id = (SELECT e.est_id FROM estacion e) AND f.var_id_id = (SELECT var_id FROM variable)
            AND f.fre_fecha_ini <= ta.dia
            AND (f.fre_fecha_fin >= ta.dia OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1) as numero_datos_esperado
        FROM tabla_acumulada ta ORDER by ta.dia
    ),
    tabla_calculo AS (
        SELECT tde.dia, tde.numero_datos, tde.numero_datos_esperado,
        ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) as porcentaje,
        CASE WHEN ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) < (SELECT umbral_completo FROM variable)
        OR ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) > 100 THEN TRUE ELSE FALSE END AS porcentaje_error
        FROM tabla_datos_esperados tde
    ),
    tabla_valores_sos AS (
        SELECT ta.dia,
            (SELECT COUNT(tb.valor) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.valor>29.0 OR tb.valor < 3.0 )
            )::numeric as numero_valor_sospechoso,
            (SELECT COUNT(tb.maximo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.maximo>29.0 OR tb.maximo < 3.0 )
            )::numeric as numero_maximo_sospechoso,
            (SELECT COUNT(tb.minimo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.minimo>29.0 OR tb.minimo < 3.0 )
            )::numeric as numero_minimo_sospechoso
        FROM tabla_acumulada ta ORDER BY ta.dia
    ),
    tabla_varia_err AS (
        SELECT ta.dia,
            (SELECT COUNT(tv.variacion_consecutiva) nsvalor FROM tabla_variacion tv WHERE date(tv.fecha) = ta.dia
                AND (tv.variacion_consecutiva <= -(select abs(var_err) from variable where var_id = 2) )
            )::numeric as varia_error
        FROM tabla_acumulada ta ORDER BY ta.dia
    ),
    -- revision de lapsos de tiempo entre fechas
    lapsos_dias AS (
        SELECT
            ff.dia,
            row_number() OVER (ORDER BY ff.dia ASC) as fecha_grupo,
            EXTRACT(EPOCH FROM ff.dia - lag(ff.dia) OVER (ORDER BY ff.dia ASC))/86400 as lapso_tiempo
        FROM (SELECT tc.dia FROM tabla_calculo tc) ff ORDER BY dia ASC
    ),
    error_lapsos AS (
        SELECT *,
            CASE WHEN fecha_grupo = 1 THEN 1 ELSE
            CASE WHEN lapso_tiempo < 1 THEN 0
                 WHEN lapso_tiempo > 1 THEN 3
                 WHEN LEAD (lapso_tiempo) OVER (ORDER BY ld.dia) > 1 THEN 2
                ELSE 1
            END
        END AS fecha_valida
        FROM lapsos_dias ld
    ),
    reporte AS (
        SELECT
        row_number() OVER (ORDER BY ta.dia ASC) as id,
        ta.dia, 
        (SELECT el.fecha_valida FROM error_lapsos el WHERE el.dia = ta.dia)::numeric as dia_error,
        (SELECT SUM(td.num_duplicados) FROM tabla_duplicados td WHERE td.dia = ta.dia)::numeric as fecha_numero,
        ROUND(ta.valor,2)::numeric as valor, ROUND(ta.maximo,2)::numeric as maximo, ROUND(ta.minimo,2)::numeric as minimo,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        (SELECT tc.porcentaje_error FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje_error,
        --ta.valor > 29.0 OR ta.valor < 3.0 AS valor_error,
        --ta.maximo > 29.0 OR ta.maximo < 3.0 AS maximo_error,
        --ta.minimo > 29.0 OR ta.minimo < 3.0 AS minimo_error,
        CASE WHEN (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        CASE WHEN (SELECT tvs.numero_maximo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        CASE WHEN (SELECT tvs.numero_minimo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as valor_numero,
        (SELECT tvs.numero_maximo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as maximo_numero,
        (SELECT tvs.numero_minimo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as minimo_numero,
        ROUND((SELECT AVG(dp.valor) FROM diario_var2diario dp WHERE dp.estacion_id = (SELECT est_id FROM estacion) AND
            date_part('day',dp.fecha)= date_part('day', ta.dia) AND date_part('month',dp.fecha)= date_part('month',ta.dia)),2) as media_historica,

        TRUE as estado,
        ta.existe_en_validacion as validado,
		(select tve.varia_error from tabla_varia_err tve where tve.dia = ta.dia) as c_varia_err
        FROM tabla_acumulada ta

    )
    SELECT * FROM reporte;


"""
