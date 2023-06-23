import calendar
import decimal as dec
from datetime import date, datetime, time, timedelta
from threading import Thread

import numpy as np
import pandas as pd
from django.apps import apps
from django.db.models import BooleanField, IntegerField, Value

from station.models import DeltaT, Station
from variable.models import Variable

threads_report_calculation = []


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
    report, selected, measurement, validated = daily_report(
        station, variable, start_time, end_time, minimum, maximum
    )
    # reporte, series = calculo_reporte_diario(station, variable, start_time, end_time, maximum, minimum)
    # reporte.rename(
    #     columns={
    #         "date": "fecha",
    #         "date_error": "fecha_error",
    #         # 'repeated_values_count':'fecha_numero',
    #         "extra_data_count": "fecha_numero",
    #         "avg_value": "valor",
    #         "max_maximum": "maximo",
    #         "min_minimum": "minimo",
    #         "percentage": "porcentaje",
    #         # TODO Confirm if "is_null" must be replaced for "porcentaje_error"
    #         # "is_null": "porcentaje_error",
    #         "percentage_error": "porcentaje_error",
    #         "value_error": "valor_error",
    #         "maximum_error": "maximo_error",
    #         "minimum_error": "minimo_error",
    #         "suspicious_values_count": "valor_numero",
    #         "suspicious_maximums_count": "maximo_numero",
    #         "suspicious_minimums_count": "minimo_numero",
    #         "historic_diary_avg": "media_historica",
    #         "state": "estado",
    #         "all_validated": "validado",
    #         "value_difference_error_count": "c_varia_err",
    #     },
    #     inplace=True,
    # )

    # # response = acumulado.to_dict(orient='list')
    # # response = _records.to_dict(orient='records')
    # if variable.variable_id in [4, 5]:
    #     report["n_valor"] = 0
    # else:
    #     report["n_valor"] = report["c_varia_err"]
    if variable.variable_id in [4, 5]:
        report["n_value"] = 0
    else:
        report["n_value"] = report["value_difference_error_count"]

    # num_fecha = len(
    #     report[report["fecha_error"].ne(1) & ~report["fecha_error"].isna()].index
    # )
    num_date = len(
        report[report["date_error"].ne(1) & ~report["date_error"].isna()].index
    )

    # num_porcentaje = len(report[report["porcentaje_error"].eq(True)])
    num_percentage = len(report[report["percentage_error"].eq(True)])

    # num_valor = len(
    #     report[report["porcentaje_error"].eq(False) & ~report["valor_numero"].isna()]
    # )
    num_value = len(
        report[
            report["percentage_error"].eq(False)
            & ~report["suspicious_values_count"].isna()
        ]
    )

    # num_maximo = len(
    #     report[
    #         report["porcentaje_error"].eq(False) & ~report["maximo_numero"].isna()
    #     ]
    # )
    num_maximum = len(
        report[
            report["percentage_error"].eq(False)
            & ~report["suspicious_maximums_count"].isna()
        ]
    )

    # num_minimo = len(
    #     report[
    #         report["porcentaje_error"].eq(False) & ~report["minimo_numero"].isna()
    #     ]
    # )
    num_minimum = len(
        report[
            report["percentage_error"].eq(False)
            & ~report["suspicious_minimums_count"].isna()
        ]
    )

    # num_dias = len(report.index)
    num_days = len(report.index)

    data = {
        # "estacion": [
        "station": [
            {
                # "est_id": station.station_id,
                "id": station.station_id,
                # "est_nombre": station.station_name,
                "name": station.station_name,
            }
        ],
        "variable": [
            {
                # "var_id": variable.variable_id,
                "id": variable.variable_id,
                # "var_nombre": variable.name,
                "name": variable.name,
                # "var_maximo": variable.maximum,
                "maximum": variable.maximum,
                # "var_minimo": variable.minimum,
                "minimum": variable.minimum,
                # "var_unidad_sigla": variable.unit.initials,
                "unit_initials": variable.unit.initials,
                # "es_acumulada": variable.is_cumulative,
                "is_cumulative": variable.is_cumulative,
            }
        ],
        # "datos": reporte.fillna("").to_dict(orient="records"),
        "data": report.fillna("").to_dict(orient="records"),
        # "indicadores": [
        "indicators": [
            {
                # "num_fecha": num_fecha,
                "num_date": num_date,
                # "num_porcentaje": num_porcentaje,
                "num_percentage": num_percentage,
                # "num_valor": num_valor,
                "num_value": num_value,
                # "num_maximo": num_maximo,
                "num_maximum": num_maximum,
                # "num_minimo": num_minimo,
                "num_minimum": num_minimum,
                # "num_dias": num_dias,
                "num_days": num_days,
            }
        ],
        # "datos_grafico": selected.fillna("").values.tolist(),  # datos_grafico,
        "plot_data": selected.fillna("").values.tolist(),
        "series": {
            "selected": selected.fillna("").to_dict("list"),
            "measurement": measurement.fillna("").to_dict("list"),
            "validated": validated.fillna("").to_dict("list"),
        },
        # "grafico": None,  # grafico_msj,
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
        (joined["value"] < minimum) | (joined["value"] > maximum),
        True,
        False
        # (joined["value"] < minimum) | (joined["value"] > maximum), 1, 0
    )
    joined["suspicious_maximum"] = np.where(
        (joined["maximum"] < minimum) | (joined["maximum"] > maximum),
        True,
        False
        # (joined["maximum"] < minimum) | (joined["maximum"] > maximum), 1, 0
    )
    joined["suspicious_minimum"] = np.where(
        (joined["minimum"] < minimum) | (joined["minimum"] > maximum),
        True,
        False
        # (joined["minimum"] < minimum) | (joined["minimum"] > maximum), 1, 0
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
    daily["percentage"] = (daily["data_count"] / expected_data_count) * 100.0
    # TODO escoger la correcta para PARICIA
    daily["is_null"] = daily["percentage"] < (100.0 - float(variable.null_limit))
    # daily['is_null'] = daily['percentage'] < variable.null_limit

    daily["percentage_error"] = ~daily["percentage"].between(
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
    daily["suspicious_values_count"] = daily_group["suspicious_value"].sum().to_numpy()

    # daily['suspicious_maximums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='maximum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily["suspicious_maximums_count"] = (
        daily_group["suspicious_maximum"].sum().to_numpy()
    )

    # daily['suspicious_minimums_count'] = daily_group.agg(
    #     suspicious=pd.NamedAgg(
    #         column='minimum',
    #         aggfunc=lambda x: (x < variable.var_minimo).sum() + (x > variable.var_maximo).sum()
    #     )).to_numpy()
    daily["suspicious_minimums_count"] = (
        daily_group["suspicious_minimum"].sum().to_numpy()
    )

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
                "percentage",
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

    # porcentaje : percentage
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
        where=["(date_part('month', time), date_part('day', time)) in %s"],
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
    daily["percentage"].fillna(0, inplace=True)
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
    daily["percentage"] = daily["percentage"].astype(np.float64).round(1)

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
def detail_list(station_id, variable_id, date, minimum, maximum):
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
    num_date = len(_selected[_selected["time_lapse_status"] != 1].index)

    # Only take into account 'value_error' when there's no error in timestamp lapse
    _selected_NO_TIMELAPSE_ERROR = _selected[_selected["time_lapse_status"] == 1]
    # num_valor = len(
    #     _selected_NO_TIMELAPSE_ERROR[
    #         _selected_NO_TIMELAPSE_ERROR["value_error"] == True
    #     ].index
    # )
    # num_maximo = len(_selected[_selected["maximum_error"] == True].index)
    # num_minimo = len(_selected[_selected["minimum_error"] == True].index)

    num_value = len(
        _selected_NO_TIMELAPSE_ERROR[
            _selected_NO_TIMELAPSE_ERROR["suspicious_value"] == True
        ].index
    )
    num_maximum = len(_selected[_selected["suspicious_maximum"] == True].index)
    num_minimum = len(_selected[_selected["suspicious_minimum"] == True].index)

    num_stddev = len(_selected[_selected["stddev_error"] == True].index)

    # TODO check if this es expected number of data
    num_data = int(24 * (60 / tx_period))

    # report.rename(
    #     columns={
    #         # 'id': '',
    #         "time": "fecha",
    #         "value": "valor",
    #         "maximum": "maximo",
    #         "minimum": "minimo",
    #         "is_validated": "validado",
    #         "is_selected": "seleccionado",
    #         "state": "estado",
    #         "time_lapse_status": "fecha_error",
    #         # "value_error": "valor_error",
    #         # "maximum_error": "maximo_error",
    #         # "minimum_error": "minimo_error",
    #         "suspicious_value": "valor_error",
    #         "suspicious_maximum": "maximo_error",
    #         "suspicious_minimum": "minimo_error",
    #         "stddev_error": "stddev_error",
    #         "comment": "comentario",
    #         "value_difference": "variacion_consecutiva",
    #         "value_difference_error": "varia_error",
    #     },
    #     inplace=True,
    # )

    # data = {
    #     "datos": report.to_dict(orient="records"),
    #     "indicadores": [
    #         {
    #             "num_fecha": num_fecha,
    #             "num_valor": num_valor,
    #             "num_valor1": num_valor,
    #             "num_maximo": num_maximo,
    #             "num_minimo": num_minimo,
    #             "num_stddev": num_stddev,
    #             "num_datos": num_datos,
    #         }
    #     ],
    # }

    data = {
        "series": report.to_dict(orient="records"),
        "indicators": [
            {
                "num_date": num_date,
                "num_value": num_value,
                # "num_valor1": num_value,
                "num_maximum": num_maximum,
                "num_minimum": num_minimum,
                "num_stddev": num_stddev,
                "num_data": num_data,
            }
        ],
    }

    return data


def get_conditions(changes_list):
    dates_condition = []
    dates_delete = []
    for row in changes_list:
        # TODO check "validado" has equivalence
        # if fila["validado"]:
        #     fechas_condicion.append("'" + fila["fecha"] + "'")
        if not row["state"]:
            dates_delete.append("'" + row["date"] + "'")

    dates_condition = set(dates_condition)
    dates_delete = set(dates_delete)

    where_dates = ",".join(dates_condition)
    where_delete = ",".join(dates_delete)

    conditions = {"where_delete": where_delete, "where_dates": where_dates}
    return conditions


# Pasar los datos crudos a validados
def save_to_validated(changes_list, variable, station, conditions, minimum, maximum):
    Measurement = apps.get_model(
        app_label="measurement", model_name=variable.variable_code
    )
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)

    # where_fechas = condiciones.get('where_fechas')
    start_date = changes_list[0]["date"]
    end_date = changes_list[-1]["date"]
    start_date, end_date = set_time_limits(start_date, end_date)

    # TODO se puede eliminar
    reporte_recibido = pd.DataFrame.from_records(changes_list)

    measurement, validated, joined, selected, tx_period = basic_calculations(
        station, variable, start_date, end_date, minimum, maximum
    )
    if len(conditions["where_delete"]) > 0:
        where_delete = conditions["where_delete"].replace("'", "").split(",")
        for _date in where_delete:
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
    if len(insert_result) != len(selected):
        return False
    launch_report_calculations()
    return True


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


def data_report(temporality, station, variable, start_time, end_time):
    start_time, end_time = set_time_limits(start_time, end_time)
    if temporality not in ["measurement", "validated", "hourly", "daily", "monthly"]:
        return None
    Data = apps.get_model(app_label=temporality, model_name=variable.variable_code)
    data = Data.objects.filter(
        station_id=station.station_id, time__gte=start_time, time__lte=end_time
    ).order_by("time")

    data_columns = [e.name for e in data.model._meta.fields]
    allowed_fields = ("sum", "average", "minimum", "maximum", "value", "total")
    value_fields = [e for e in data_columns if e in allowed_fields]
    base_fields = [
        "time",
    ]
    fields = base_fields + value_fields
    df = pd.DataFrame.from_records(data.values(*fields))
    if df.empty:
        df = pd.DataFrame(columns=fields)
    return df


def dict_data_report(temporality, station, variable, start_time, end_time):
    df = data_report(temporality, station, variable, start_time, end_time)
    response = {
        "station": {
            "id": station.station_id,
            "code": station.station_code,
        },
        "variable": {
            "id": variable.variable_id,
            "name": variable.name,
            "maximum": variable.maximum,
            "minimum": variable.minimum,
            "unit_initials": variable.unit.initials,
            "is_cumulative": variable.is_cumulative,
        },
        "series": df.fillna("").to_dict("list"),
        "temporality": temporality,
    }
    return response


def csv_data_report(temporality, station, variable, start_time, end_time):
    df = data_report(temporality, station, variable, start_time, end_time)
    csv_response = df.to_csv(index=False)
    return csv_response


def calculate_reports(variable):
    global threads_report_calculation
    threads_report_calculation.append(variable.variable_id)
    calculate_hourly(variable)
    calculate_daily(variable)
    calculate_monthly(variable)
    threads_report_calculation.remove(variable.variable_id)


def thread_launch_report_calculations():
    global threads_report_calculation
    variables = Variable.objects.all()
    for variable in variables:
        if not variable.automatic_report:
            continue
        attempt = 0
        while variable.variable_id in threads_report_calculation:
            time.sleep(10)
            attempt = attempt + 1
            if attempt > 5:
                break
        calculate_reports(variable)


def launch_report_calculations():
    global threads_report_calculation
    if len(threads_report_calculation) > 0:
        return
    t = Thread(target=thread_launch_report_calculations, args=())
    t.start()


def calculate_hourly(variable):
    Validated = apps.get_model(app_label="validated", model_name=variable.variable_code)
    Hourly = apps.get_model(app_label="hourly", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Validated.objects.filter(used_for_hourly=False).first()
        if not register:
            register_exists = False
            return False

        start_of_hour = datetime.combine(
            register.time, time(register.time.hour, 0, 0, 0)
        )
        end_of_hour = datetime.combine(
            register.time, time(start_of_hour.hour, 59, 59, 999999)
        )
        validated_block = Validated.objects.filter(
            station_id=register.station_id,
            time__gte=start_of_hour,
            time__lte=end_of_hour,
        )
        data_columns = [e.name for e in validated_block.model._meta.fields]
        allowed_fields = ("sum", "value", "average")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(validated_block.values(*fields))
        if block.empty:
            continue

        if "sum" in fields:
            _sum = block["sum"].sum()
            count = block["sum"].count()
        else:
            # else: is average
            average = block["average"].mean(skipna=True)
            count = block["average"].count()

        try:
            delta_t = DeltaT.objects.get(station__station_id=register.station_id)
        except:
            return False

        completeness = (count / (60 / delta_t.delta_t)) * 100.0
        Hourly.objects.filter(
            time=start_of_hour, station_id=register.station_id
        ).delete()

        if "sum" in fields:
            hourly = Hourly(
                time=start_of_hour,
                station_id=register.station_id,
                used_for_daily=False,
                completeness=completeness,
                sum=_sum,
            )
        else:
            hourly = Hourly(
                time=start_of_hour,
                station_id=register.station_id,
                used_for_daily=False,
                completeness=completeness,
                average=average,
            )
        hourly.save()
        validated_block.update(used_for_hourly=True)
    return True


def calculate_daily(variable):
    Hourly = apps.get_model(app_label="hourly", model_name=variable.variable_code)
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Hourly.objects.filter(used_for_daily=False).first()
        if not register:
            register_exists = False
            return

        start_of_day = datetime.combine(register.time, time(0, 0, 0, 0))
        end_of_day = datetime.combine(register.time, time(23, 59, 59, 999999))
        hourly_block = Hourly.objects.filter(
            station_id=register.station_id, time__gte=start_of_day, time__lte=end_of_day
        )
        data_columns = [e.name for e in hourly_block.model._meta.fields]
        allowed_fields = ("sum", "average", "total")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(hourly_block.values(*fields))
        if block.empty:
            continue
        if "sum" in fields:
            _sum = block["sum"].sum()
            count = block["sum"].count()
        else:
            # else: is average
            average = block["average"].mean(skipna=True)
            count = block["average"].count()
        completeness = (count / 24) * 100.0
        Daily.objects.filter(time=start_of_day, station_id=register.station_id).delete()
        if "sum" in fields:
            daily = Daily(
                time=start_of_day,
                station_id=register.station_id,
                used_for_monthly=False,
                completeness=completeness,
                sum=_sum,
            )
        else:
            daily = Daily(
                time=start_of_day,
                station_id=register.station_id,
                used_for_monthly=False,
                completeness=completeness,
                average=average,
            )
        daily.save()
        hourly_block.update(used_for_daily=True)


def calculate_monthly(variable):
    Daily = apps.get_model(app_label="daily", model_name=variable.variable_code)
    Monthly = apps.get_model(app_label="monthly", model_name=variable.variable_code)
    register_exists = True
    while register_exists:
        register = Daily.objects.filter(used_for_monthly=False).first()
        if not register:
            register_exists = False
            return

        start_of_month = datetime(register.time.year, register.time.month, 1, 0, 0)
        last_day = calendar.monthrange(register.time.year, register.time.month)[1]
        end_of_month = datetime(
            register.time.year, register.time.month, last_day, 23, 59
        )
        daily_block = Daily.objects.filter(
            station_id=register.station_id,
            time__gte=start_of_month,
            time__lte=end_of_month,
        )
        data_columns = [e.name for e in daily_block.model._meta.fields]
        allowed_fields = ("minimum", "maximum", "value", "average", "total")
        value_fields = [e for e in data_columns if e in allowed_fields]
        base_fields = [
            "time",
        ]
        fields = base_fields + value_fields
        block = pd.DataFrame.from_records(daily_block.values(*fields))
        if block.empty:
            continue
        if "sum" in fields:
            _sum = block["sum"].sum()
            count = block["sum"].count()
        else:
            # else: is average
            average = block["average"].mean(skipna=True)
            count = block["average"].count()
        completeness = (count / last_day) * 100.0
        Monthly.objects.filter(
            time=start_of_month, station_id=register.station_id
        ).delete()
        if "sum" in fields:
            monthly = Monthly(
                time=start_of_month,
                station_id=register.station_id,
                completeness=completeness,
                sum=_sum,
            )
        else:
            monthly = Monthly(
                time=start_of_month,
                station_id=register.station_id,
                completeness=completeness,
                average=average,
            )
        monthly.save()
        daily_block.update(used_for_monthly=True)
