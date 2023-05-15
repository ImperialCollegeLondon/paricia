# from diario.models import Var2Diario
import decimal as dec
from datetime import date, datetime, time, timedelta

import numpy as np
import pandas as pd

# from estacion.models import Estacion
from django.apps import apps
from django.db.models import BooleanField, IntegerField, Value

from station.models import Station
from variable.models import Variable


def set_time_limits(start_time, end_time):
    if isinstance(start_time, date):
        start_time = datetime.combine(start_time, time(0, 0, 0, 0))
    elif isinstance(start_time, str):
        start_time = start_time + " 00:00:00"

    if isinstance(end_time, date):
        end_time = datetime.combine(end_time, time(23, 59, 59, 999999))
    elif isinstance(end_time, str):
        end_time = end_time + " 23:59:59"
    return start_time, end_time


def daily_validation(station, variable, start_time, end_time, minimum, maximum):
    reporte, selected, measurement, validated = daily_report(
        station, variable, start_time, end_time, minimum, maximum
    )
    # reporte, series = calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum)
    reporte.rename(
        columns={
            "date": "fecha",
            "date_error": "fecha_error",
            # 'repeated_values_count':'fecha_numero',
            "extra_data_count": "fecha_numero",
            "avg_value": "valor",
            "max_maximum": "maximo",
            "min_minimum": "minimo",
            "data_existence_percentage": "porcentaje",
            # TODO Confirm if "is_null" must be replaced for "porcentaje_error"
            # "is_null": "porcentaje_error",
            "percentage_error": "porcentaje_error",
            "value_error": "valor_error",
            "maximum_error": "maximo_error",
            "minimum_error": "minimo_error",
            "suspicious_values_count": "valor_numero",
            "suspicious_maximums_count": "maximo_numero",
            "suspicious_minimums_count": "minimo_numero",
            "historic_diary_avg": "media_historica",
            "state": "estado",
            "all_validated": "validado",
            "value_difference_error_count": "c_varia_err",
        },
        inplace=True,
    )

    # response = acumulado.to_dict(orient='list')
    # response = _records.to_dict(orient='records')
    if variable.variable_id in [4, 5]:
        reporte["n_valor"] = 0
    else:
        reporte["n_valor"] = reporte["c_varia_err"]
    num_fecha = len(
        reporte[reporte["fecha_error"].ne(1) & ~reporte["fecha_error"].isna()].index
    )
    num_porcentaje = len(reporte[reporte["porcentaje_error"].eq(True)])
    num_valor = len(
        reporte[reporte["porcentaje_error"].eq(False) & ~reporte["valor_numero"].isna()]
    )
    num_maximo = len(
        reporte[
            reporte["porcentaje_error"].eq(False) & ~reporte["maximo_numero"].isna()
        ]
    )
    num_minimo = len(
        reporte[
            reporte["porcentaje_error"].eq(False) & ~reporte["minimo_numero"].isna()
        ]
    )
    num_dias = len(reporte.index)

    data = {
        "estacion": [
            {
                "est_id": station.station_id,
                "est_nombre": station.station_name,
            }
        ],
        "variable": [
            {
                "var_id": variable.variable_id,
                "var_nombre": variable.name,
                "var_maximo": variable.maximum,
                "var_minimo": variable.minimum,
                "var_unidad_sigla": variable.unit.initials,
                "es_acumulada": variable.is_cumulative,
            }
        ],
        "datos": reporte.fillna("").to_dict(orient="records"),
        "indicadores": [
            {
                "num_fecha": num_fecha,
                "num_porcentaje": num_porcentaje,
                "num_valor": num_valor,
                "num_maximo": num_maximo,
                "num_minimo": num_minimo,
                "num_dias": num_dias,
            }
        ],
        "datos_grafico": selected.fillna("").values.tolist(),  # datos_grafico,
        "series": {
            "selected": selected.fillna("").to_dict("list"),
            "measurement": measurement.fillna("").to_dict("list"),
            "validated": validated.fillna("").to_dict("list"),
        },
        "grafico": None,  # grafico_msj,
        "curva": None,  # mensaje
    }
    return data


# Basic calculations is the main functions for calculations
def basic_calculations(station, variable, start_time, end_time, minimum, maximum):
    # TODO change tx_period for the code to query from model
    tx_period = 5
    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    validated = (
        Validated.objects.filter(
            station_id=station.station_id, time__gte=start_time, time__lte=end_time
        )
        .annotate(
            # is_validated: True is for 'validated' tables, False for raw 'measurement'
            is_validated=Value(True, output_field=BooleanField()),
            exists_in_validated=Value(True, output_field=BooleanField()),
            null_value=Value(False, output_field=BooleanField()),
        )
        .order_by("time")
    )

    value_fields = ("value", "minimum", "maximum")
    base_fields = ("id", "time", "is_validated", "exists_in_validated", "null_value")
    fields = base_fields + value_fields
    validated = pd.DataFrame.from_records(validated.values(*fields))

    if validated.empty:
        validated = pd.DataFrame(columns=fields)

    # validated.replace(to_replace=[None], value=np.nan, inplace=True)

    # TODO WHich one is faster?
    # validated['time'] = validated['time'].values.astype('<M8[m]')
    # TODO for testing: time_truncated
    validated["time_truncated"] = validated["time"].values.astype("<M8[m]")
    # validated['time_truncated2'] = pd.to_datetime(validated['time']).dt.date
    # validated['time_truncated3'] = validated['time'].dt.floor('min')

    measurement = (
        Measurement.objects.filter(
            station_id=station.station_id, time__gte=start_time, time__lte=end_time
        )
        .annotate(
            # is_validated: True is for 'validated' tables, False for raw 'measurement'
            is_validated=Value(False, output_field=BooleanField()),
        )
        .order_by("time")
    )

    value_fields = ("value", "minimum", "maximum")
    base_fields = ("id", "time", "is_validated")
    fields = base_fields + value_fields
    measurement = pd.DataFrame.from_records(measurement.values(*fields))

    if measurement.empty:
        measurement = pd.DataFrame(columns=fields)
    measurement["time_truncated"] = measurement["time"].values.astype("<M8[m]")
    # measurement['time_truncated2'] = pd.to_datetime(measurement['time']).dt.date
    # measurement['time_truncated3'] = measurement['time'].dt.floor('min')

    # TODO analizar eliminacion campos 'null_value' : parece ser innecesario o fácilmente eliminable
    # measurement['null_value'] = measurement['time_truncated'].isin(validated['time_truncated'])
    # TODO Probabliy is not necessary to math 'time' and 'value'
    # matches_time_and_value = pd.merge(measurement, validated, on=['time_truncated', 'value'], how='outer', indicator=True)

    # TODO IMPORTANT: Verify all of matches_time and 'exists_in_validated' computations
    matches_time = pd.merge(
        measurement, validated, on=["time_truncated"], how="outer", indicator=True
    )
    # TODO Specially, Check the following line: It´s not doing the right thing.
    measurement["exists_in_validated"] = matches_time["_merge"] == "both"

    joined = pd.concat([validated, measurement]).sort_values(
        by=["time_truncated", "is_validated", "id"], ascending=[True, False, False]
    )
    joined["date"] = pd.to_datetime(joined["time"]).dt.date
    joined.rename(columns={"id": "db_row_id"}, inplace=True)
    joined.reset_index(drop=True, inplace=True)

    joined.index.name = "id_joined"
    joined.reset_index(inplace=True)
    # joined.reset_index(names='id_joined', inplace=True)

    minimum = float(minimum)
    maximum = float(maximum)
    joined["suspicious_value"] = np.where(
        (joined["value"] < minimum) | (joined["value"] > maximum), True, False
    )
    joined["suspicious_maximum"] = np.where(
        (joined["maximum"] < minimum) | (joined["maximum"] > maximum), True, False
    )
    joined["suspicious_minimum"] = np.where(
        (joined["minimum"] < minimum) | (joined["minimum"] > maximum), True, False
    )

    # selected
    # TODO check if 'is_selected' is used in later
    selected = joined.drop_duplicates("time_truncated", keep="first")
    selected.reset_index(drop=True, inplace=True)
    selected["is_selected"] = True
    joined = joined.merge(
        selected[["id_joined", "is_selected"]],
        on="id_joined",
        how="left",
        indicator=False,
    )
    joined["is_selected"].fillna(False, inplace=True)

    # Moved from original to reuse code
    # TODO Ask if using 'time_truncated' is better option
    selected["time_lapse"] = selected["time_truncated"] - selected[
        "time_truncated"
    ].shift(1)
    selected["time_lapse"] = selected["time_lapse"].dt.total_seconds() / 60
    selected["time_lapse_status"] = np.where(
        selected["time_lapse"] < tx_period,
        0,
        np.where(
            selected["time_lapse"] == tx_period,
            1,
            2
            # TODO check again, in validation_report too
            # When is 2 or 3
        ),
    )
    selected["time_lapse_status"][0] = 1

    selected["lagged_value"] = np.where(
        selected["time_lapse_status"].le(1),
        selected["value"].shift(1),
        np.nan,
    )

    joined = joined.merge(
        selected[["time_truncated", "time_lapse_status", "lagged_value"]],
        on="time_truncated",
        how="left",
        indicator=False,
    )
    joined["value_difference"] = joined["value"] - joined["lagged_value"]
    # TODO implement to a error/warning level (variable.diff_error and variable.diff_warning)
    joined["value_difference_error"] = np.where(
        joined["value_difference"].abs().gt(variable.diff_error),
        True,  # Error
        False,  # No Error
    )
    # # TODO Basic statistics
    # mean = selected['value'].mean(skipna=True)
    # std_dev = selected['value'].astype(float).std(skipna=True)
    # stddev_inf_limit = mean - (std_dev * float(variable.var_min))
    # stddev_sup_limit = mean + (std_dev * float(variable.var_min))
    return measurement, validated, joined, selected, tx_period


# def calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum):
def daily_report(station, variable, start_time, end_time, minimum, maximum):
    start_time, end_time = set_time_limits(start_time, end_time)
    measurement, validated, joined, selected, tx_period = basic_calculations(
        station, variable, start_time, end_time, minimum, maximum
    )

    # TODO: implement all for
    daily_group_all = joined.groupby("date")

    # REF. NAME: tabla_acumulada
    # daily calculations
    daily_group = selected.groupby("date")
    daily = daily_group["date"].count()
    daily = daily.reset_index(name="data_count")
    # daily['date'] = pd.to_datetime(daily['date']).dt.date
    # TODO Ask if those aggregation functions must be calculated over 'selected' table instead of 'joined'
    daily["avg_value"] = daily_group["value"].mean().to_numpy()
    daily["max_maximum"] = daily_group["maximum"].max().to_numpy()
    daily["min_minimum"] = daily_group["minimum"].min().to_numpy()
    daily["all_validated"] = daily_group["is_validated"].all().to_numpy()

    # REF. NAME: tabla_datos_esperados
    # Expected data count for each day. Uses "period"
    # TODO Create a "period" table for storing the period for every station
    # TODO Maybe program for dynamic periods. This happens when a station change the period

    expected_data_count = 24 * 60 / tx_period

    # REF. NAME: tabla_calculo
    # Percentage of data existence
    daily["data_existence_percentage"] = (
        daily["data_count"] / expected_data_count
    ) * 100.0
    # TODO escoger la correcta para PARICIA
    daily["is_null"] = daily["data_existence_percentage"] < (
        100.0 - float(variable.null_limit)
    )
    # daily['is_null'] = daily['data_existence_percentage'] < variable.null_limit

    daily["percentage_error"] = ~daily["data_existence_percentage"].between(
        100.0 - float(variable.null_limit), 100.0
    )

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
    daily["suspicious_values_count"] = daily_group["suspicious_value"].count()
    # daily['suspicious_maximums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='maximum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily["suspicious_maximums_count"] = daily_group["suspicious_maximum"].count()
    # daily['suspicious_minimums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='minimum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily["suspicious_minimums_count"] = daily_group["suspicious_minimum"].count()

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
    daily["value_difference_error_count"] = (
        daily_group_all["value_difference_error"].sum(numeric_only=False).to_numpy()
    )

    # # REF. NAME: lapsos_dias
    # # Generate a sequence of days following in the calendar to compare with data in database and note voids
    # # TODO Analizar que esto pudiera ser incluído en la primera generación de daily
    # calendar_day_seq = pd.DataFrame(
    #     pd.date_range(start=start_time, end=end_time).date,
    #     columns=['date']
    # )
    # daily = calendar_day_seq.merge(daily, on='date', how='left')

    if daily.empty:
        daily = df = pd.DataFrame(
            columns=[
                "id",
                "date",
                "data_count",
                "avg_value",
                "max_maximum",
                "min_minimum",
                "all_validated",
                "data_existence_percentage",
                "is_null",
                "suspicious_values_count",
                "suspicious_maximums_count",
                "suspicious_minimums_count",
                "value_difference_error_count",
                "day_interval",
                "date_error",
                "extra_data_count",
                "historic_diary_avg",
                "state",
                "value_error",
                "maximum_error",
                "minimum_error",
            ]
        )
        return daily, selected[["time", "value"]]

    # REF. NAME: fecha_error o dia_error
    daily["day_interval"] = (daily["date"] - daily["date"].shift(1)).dt.days
    daily["day_interval"][0] = 1
    daily["date_error"] = np.where(daily["day_interval"].gt(1), 3, 1)
    # TODO hacer un groupby de repeated_values_count por día, para pasar el valor total de repetidos por día
    #      posiblemente convenga hacer un solo cálculo arriba

    # fecha_numero: repeated_values_count
    # # REF. NAME: tabla_duplicados
    # # count_of_repeated
    repeated_in_validated = validated.groupby(["time_truncated"])[
        "time_truncated"
    ].count()
    repeated_in_validated = repeated_in_validated.reset_index(
        name="repeated_in_validated"
    )
    repeated_in_validated["repeated_in_validated"] = np.where(
        repeated_in_validated["repeated_in_validated"].gt(0),
        repeated_in_validated["repeated_in_validated"] - 1,
        0,
    )

    repeated_in_measurement = measurement.groupby(["time_truncated"])[
        "time_truncated"
    ].count()
    repeated_in_measurement = repeated_in_measurement.reset_index(
        name="repeated_in_measurement"
    )
    repeated_in_measurement["repeated_in_measurement"] = np.where(
        repeated_in_measurement["repeated_in_measurement"].gt(0),
        repeated_in_measurement["repeated_in_measurement"] - 1,
        0,
    )
    extra_data_count = pd.merge(
        repeated_in_validated,
        repeated_in_measurement,
        on=["time_truncated"],
        how="outer",
        indicator=False,
    )
    extra_data_count.fillna(0, inplace=True)
    extra_data_count.sort_values(by=["time_truncated"], inplace=True)
    extra_data_count["extra_values_count"] = (
        extra_data_count["repeated_in_validated"]
        + extra_data_count["repeated_in_measurement"]
    )
    extra_data_count["date"] = pd.to_datetime(
        extra_data_count["time_truncated"]
    ).dt.date

    extra_data_daily_group = extra_data_count[
        extra_data_count["extra_values_count"] > 0
    ].groupby("date")
    extra_data_daily = extra_data_daily_group["extra_values_count"].sum()
    extra_data_daily = extra_data_daily.reset_index(name="extra_data_count")
    daily = daily.merge(extra_data_daily, on="date", how="left")
    daily["extra_data_count"].fillna(0, inplace=True)

    # TODO the following line makes an override of "date_error"
    #           Discuss if the team are agree
    daily["date_error"] = daily["extra_data_count"]

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

    month_day_tuples = tuple(
        list(
            zip(
                pd.DatetimeIndex(daily["date"]).month,
                pd.DatetimeIndex(daily["date"]).day,
            )
        )
    )
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    historic_diary = Daily.objects.filter(station_id=station.station_id).extra(
        where=["(date_part('month', date), date_part('day', date)) in %s"],
        params=[month_day_tuples],
    )
    historic_diary = pd.DataFrame(list(historic_diary.values()))
    if not historic_diary.empty:
        historic_diary["month-day"] = (
            pd.DatetimeIndex(historic_diary["date"]).month.astype(str)
            + "-"
            + pd.DatetimeIndex(historic_diary["date"]).day.astype(str)
        )
        historic_diary_group = historic_diary.groupby(["month-day"])
        daily["historic_diary_avg"] = historic_diary_group["value"].mean().to_numpy()
    else:
        daily["historic_diary_avg"] = np.nan

    # estado : state
    daily["state"] = True

    # validado :

    # validated_only = selected[['date', 'is_validated']].loc[selected['is_validated'] == True]
    # validated_count = validated_only.groupby('date')['date'].count().reset_index(name='validated_count')
    # daily = daily.merge(validated_count, on='date', how='left')
    # daily['validated_count'].fillna(0, inplace=True)

    # daily['all_validated'] = daily_group['is_validated'].all().to_numpy()

    # c_varia_err

    daily["data_count"].fillna(0, inplace=True)
    daily["data_existence_percentage"].fillna(0, inplace=True)
    daily["suspicious_values_count"].fillna(0, inplace=True)
    daily["suspicious_maximums_count"].fillna(0, inplace=True)
    daily["suspicious_minimums_count"].fillna(0, inplace=True)
    daily["value_difference_error_count"].fillna(0, inplace=True)
    daily["historic_diary_avg"].fillna("", inplace=True)

    ##
    # TODO check, maybe it's not needed anymore
    daily["value_error"] = np.where(
        daily["suspicious_values_count"].gt(0),
        True,
        False,
    )
    daily["maximum_error"] = np.where(
        daily["suspicious_maximums_count"].gt(0),
        True,
        False,
    )
    daily["minimum_error"] = np.where(
        daily["suspicious_minimums_count"].gt(0),
        True,
        False,
    )
    #
    ##

    # Round decimals
    # TODO cambiar 'valor' por 'value' en pAricia
    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )
    decimal_places = Measurement._meta.get_field("value").decimal_places
    daily["avg_value"] = daily["avg_value"].astype(np.float64).round(decimal_places)
    daily["max_maximum"] = daily["max_maximum"].astype(np.float64).round(decimal_places)
    daily["min_minimum"] = daily["min_minimum"].astype(np.float64).round(decimal_places)
    daily["data_existence_percentage"] = (
        daily["data_existence_percentage"].astype(np.float64).round(1)
    )

    # daily.reset_index(names='id', inplace=True)
    daily.index.name = "id"
    daily.reset_index(inplace=True)
    ## TODO Eliminar o corregir ids -> id
    #
    # daily.rename(columns={'id':'ids',}, inplace=True)
    daily["ids"] = daily["id"]
    #
    ##
    _selected = selected[["time", "value", "maximum", "minimum"]]
    _measurement = measurement[["time", "value", "maximum", "minimum"]]
    _validated = validated[["time", "value", "maximum", "minimum"]]
    return daily, _selected, _measurement, _validated


# Consultar datos crudos y/o validados por estacion, variable y fecha de un día en específico
# def detalle_diario(est_id, var_id, fecha_str, sup_lim_variable, inf_lim_variable):
def detalle_diario(station_id, variable_id, date, minimum, maximum):
    # SQL fun : reporte_validacion_modelo
    # SQL template: validacion_crudos_prom.sql

    start_time = datetime.strptime(date, "%Y-%m-%d")
    end_time = datetime.combine(start_time.date(), time(23, 59, 59, 999999))
    station = Station.objects.get(station_id=station_id)
    variable = Variable.objects.get(variable_id=variable_id)

    measurement, validated, joined, selected, tx_period = basic_calculations(
        station, variable, start_time, end_time, minimum, maximum
    )

    joined["state"] = ~(
        joined["value"].isna() & joined["maximum"].isna() & joined["minimum"].isna()
    )
    # Basic statistics
    mean = selected["value"].mean(skipna=True)
    std_dev = selected["value"].astype(float).std(skipna=True)
    stddev_inf_limit = mean - (std_dev * float(variable.outlier_limit))
    stddev_sup_limit = mean + (std_dev * float(variable.outlier_limit))
    joined["stddev_error"] = ~joined["value"].between(
        stddev_inf_limit, stddev_sup_limit
    )
    joined["comment"] = ""

    joined.fillna("", inplace=True)

    report = joined[
        [
            "id_joined",
            "time",
            "value",
            "maximum",
            "minimum",
            "is_validated",
            "is_selected",
            "state",
            "time_lapse_status",
            # "value_error",
            # "maximum_error",
            # "minimum_error",
            "suspicious_value",
            "suspicious_maximum",
            "suspicious_minimum",
            "stddev_error",
            "comment",
            "value_difference",
            "value_difference_error",
        ]
    ]
    report.rename(
        columns={
            "id_joined": "id",
            "suspicious_value": "value_error",
            "suspicious_maximum": "maximum_error",
            "suspicious_minimum": "minimum_error",
        },
        inplace=True,
    )
    #######
    joined["n_valor"] = joined["value_difference"]
    _selected = joined[joined["is_selected"] == True]
    num_fecha = len(_selected[_selected["time_lapse_status"] != 1].index)

    # Only take into account 'value_error' when there's no error in timestamp lapse
    _selected_NO_TIMELAPSE_ERROR = _selected[_selected["time_lapse_status"] == 1]
    # num_valor = len(
    #     _selected_NO_TIMELAPSE_ERROR[
    #         _selected_NO_TIMELAPSE_ERROR["value_error"] == True
    #     ].index
    # )
    # num_maximo = len(_selected[_selected["maximum_error"] == True].index)
    # num_minimo = len(_selected[_selected["minimum_error"] == True].index)

    num_valor = len(
        _selected_NO_TIMELAPSE_ERROR[
            _selected_NO_TIMELAPSE_ERROR["suspicious_value"] == True
        ].index
    )
    num_maximo = len(_selected[_selected["suspicious_maximum"] == True].index)
    num_minimo = len(_selected[_selected["suspicious_minimum"] == True].index)

    num_stddev = len(_selected[_selected["stddev_error"] == True].index)

    # TODO check if this es expected number of data
    num_datos = int(24 * (60 / tx_period))

    report.rename(
        columns={
            # 'id': '',
            "time": "fecha",
            "value": "valor",
            "maximum": "maximo",
            "minimum": "minimo",
            "is_validated": "validado",
            "is_selected": "seleccionado",
            "state": "estado",
            "time_lapse_status": "fecha_error",
            # "value_error": "valor_error",
            # "maximum_error": "maximo_error",
            # "minimum_error": "minimo_error",
            "suspicious_value": "valor_error",
            "suspicious_maximum": "maximo_error",
            "suspicious_minimum": "minimo_error",
            "stddev_error": "stddev_error",
            "comment": "comentario",
            "value_difference": "variacion_consecutiva",
            "value_difference_error": "varia_error",
        },
        inplace=True,
    )

    data = {
        "datos": report.to_dict(orient="records"),
        "indicadores": [
            {
                "num_fecha": num_fecha,
                "num_valor": num_valor,
                "num_valor1": num_valor,
                "num_maximo": num_maximo,
                "num_minimo": num_minimo,
                "num_stddev": num_stddev,
                "num_datos": num_datos,
            }
        ],
    }

    return data


def get_condiciones(cambios_lista):
    fechas_condicion = []
    fechas_eliminar = []
    for fila in cambios_lista:
        if fila["validado"]:
            fechas_condicion.append("'" + fila["fecha"] + "'")
        if not fila["estado"]:
            fechas_eliminar.append("'" + fila["fecha"] + "'")

    fechas_condicion = set(fechas_condicion)
    fechas_eliminar = set(fechas_eliminar)

    where_fechas = ",".join(fechas_condicion)
    where_eliminar = ",".join(fechas_eliminar)

    condiciones = {"where_eliminar": where_eliminar, "where_fechas": where_fechas}
    return condiciones


# Pasar los datos crudos a validados
def pasar_crudos_validados(
    cambios_lista, variable, station, condiciones, minimum, maximum
):
    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    # where_fechas = condiciones.get('where_fechas')
    start_date = cambios_lista[0]["fecha"]
    end_date = cambios_lista[-1]["fecha"]
    start_date, end_date = set_time_limits(start_date, end_date)

    # TODO se puede eliminar
    reporte_recibido = pd.DataFrame.from_records(cambios_lista)

    measurement, validated, joined, selected, tx_period = basic_calculations(
        station, variable, start_date, end_date, minimum, maximum
    )
    if len(condiciones["where_eliminar"]) > 0:
        where_eliminar = condiciones["where_eliminar"].replace("'", "").split(",")
        for _date in where_eliminar:
            _date = datetime.strptime(_date, "%Y-%m-%d").date()
            condition = selected["date"] == _date
            selected["value"] = np.where(condition, None, selected["value"])
            selected["maximum"] = np.where(condition, None, selected["maximum"])
            selected["minimum"] = np.where(condition, None, selected["minimum"])
    Validated.timescale.filter(
        time__range=[start_date, end_date],
        station_id=station.station_id,
    ).delete()

    model_instances = [
        Validated(
            time=record["time"],
            value=record["value"],
            maximum=record["maximum"],
            minimum=record["minimum"],
            station_id=station.station_id,
        )
        for _, record in selected.iterrows()
    ]
    insert_result = Validated.objects.bulk_create(model_instances)
    result = False
    if len(insert_result) == len(selected):
        result = True
    return result


# def guardar_cambios_validacion(
#     estacion_id, variable, tipo_transaccion, fecha_inicio, fecha_fin
# ):
#     sincronizacion = Sincronizacion(
#         estacion_id=estacion_id,
#         variable=variable,
#         tipo_transaccion=tipo_transaccion,
#         fecha_inicio=fecha_inicio,
#         fecha_fin=fecha_fin,
#     )
#     sincronizacion.save()
