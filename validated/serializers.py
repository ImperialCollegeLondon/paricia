from rest_framework import serializers

from .models import (
    AirTemperature,
    AtmosphericPressure,
    BatteryVoltage,
    ChlorineConcentrationDepth,
    DischargeCurve,
    Flow,
    FlowManual,
    Humidity,
    IndirectRadiation,
    LevelFunction,
    OxygenConcentrationDepth,
    PercentageOxygenConcentrationDepth,
    PhycocyaninDepth,
    PolarWind,
    Precipitation,
    RedoxPotentialDepth,
    SoilMoisture,
    SoilTemperature,
    SolarRadiation,
    StripLevelReading,
    WaterAcidityDepth,
    WaterLevel,
    WaterTemperature,
    WaterTemperatureDepth,
    WaterTurbidityDepth,
    WindDirection,
    WindVelocity,
)


class PolarWindSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolarWind
        exclude = []

# TODO Confirm if DischargeCurveSerializer is not needed in Validated Models
# class DischargeCurveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DischargeCurve
#         exclude = []


# class LevelFunctionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LevelFunction
#         exclude = []


class PrecipitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precipitation
        exclude = []


class AirTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirTemperature
        exclude = []


class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Humidity
        exclude = []


class WindVelocitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WindVelocity
        exclude = []


class WindDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindDirection
        exclude = []


class SoilMoistureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilMoisture
        exclude = []


class SolarRadiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarRadiation
        exclude = []


class AtmosphericPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtmosphericPressure
        exclude = []


class WaterTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTemperature
        exclude = []


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        exclude = []


class WaterLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLevel
        exclude = []


class BatteryVoltageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatteryVoltage
        exclude = []


class FlowManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowManual
        exclude = []


class StripLevelReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripLevelReading
        exclude = []


class SoilTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilTemperature
        exclude = []


class IndirectRadiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndirectRadiation
        exclude = []


class WaterTemperatureDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTemperatureDepth
        exclude = []


class WaterAcidityDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterAcidityDepth
        exclude = []


class RedoxPotentialDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedoxPotentialDepth
        exclude = []


class WaterTurbidityDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTurbidityDepth
        exclude = []


class ChlorineConcentrationDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChlorineConcentrationDepth
        exclude = []


class OxygenConcentrationDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = OxygenConcentrationDepth
        exclude = []


class PercentageOxygenConcentrationDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageOxygenConcentrationDepth
        exclude = []


class PhycocyaninDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhycocyaninDepth
        exclude = []
