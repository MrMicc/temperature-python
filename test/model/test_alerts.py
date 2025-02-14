import pytest
from model.enum_alerts import EnumAlerts
from model.temperature import Temperature
from model.alerts import TemperatureAlert


class TestAlerts():

    @pytest.mark.parametrize("high_threshold, value", [(30.1, 30.2), (24.1, 25)])
    def test_high_temperature(self, high_threshold, value):
        alert = TemperatureAlert(high_threshold=high_threshold)
        temp = Temperature(value)
        assert alert.check(temp) == EnumAlerts.HIGH.value

    @pytest.mark.parametrize("low_threshold, value", [(0.1, -0.1), (20, 19.9), (0.1, 0.0)])
    def test_low_temperature(self, low_threshold, value):
        alert = TemperatureAlert(low_threshold=low_threshold)
        temp = Temperature(value)
        assert alert.check(temp) == EnumAlerts.LOW.value

    @pytest.mark.parametrize("low_threshold, high_threshold, value", [(20, 30, 25), (10, 20, 15)])
    def test_normal_termperature(self, low_threshold, high_threshold, value):
        alert = TemperatureAlert(
            low_threshold=low_threshold, high_threshold=high_threshold)
        temp = Temperature(value)
        assert alert.check(temp) == EnumAlerts.NORMAL.value

    @pytest.mark.parametrize("temperature, high_threshold, low_threshold, alert",
                             [(25, 25, 20, EnumAlerts.NORMAL.value),
                              (20, 25, 20, EnumAlerts.NORMAL.value)])
    def test_check_temperature(self, temperature, high_threshold, low_threshold, alert):
        temp_alert = TemperatureAlert(
            high_threshold=high_threshold, low_threshold=low_threshold)
        result = temp_alert.check(Temperature(temperature))
        assert result == alert
