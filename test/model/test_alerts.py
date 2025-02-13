from persistence.temperature_repository import SqliteTemperatureRepository
import pytest
from statistics import mean
from model.enum_alerts import EnumAlerts
from model.temperature import Temperature
from model.alerts import TemperatureAlert


class TestAlerts():
    @pytest.fixture
    def db_connection(self, tmp_path):
        db_path = tmp_path / "test_temperature.db"
        repository = SqliteTemperatureRepository(db_path)
        return repository

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

    @pytest.mark.parametrize("temperature_list, expected_alert", [
        ([Temperature(25), Temperature(25), Temperature(25)], EnumAlerts.NORMAL.value),
        ([Temperature(30), Temperature(20), Temperature(
            10), Temperature(40)], EnumAlerts.NORMAL.value),
        ([Temperature(10), Temperature(20), Temperature(
            30), Temperature(40), Temperature(45)], EnumAlerts.HIGH.value),
        ([Temperature(10), Temperature(20), Temperature(10)], EnumAlerts.LOW.value)
    ])
    def test_check_mean_temperature_alert(self, db_connection, temperature_list, expected_alert):
        for temperature in temperature_list:
            db_connection.save(temperature)
        alert = TemperatureAlert(
            high_threshold=25, low_threshold=20, repository=db_connection)
        result = alert.check_mean_temperature()

        expected_mean = mean(
            temperature.value for temperature in temperature_list)
        expected_result = {"temperature": Temperature(
            expected_mean), "alert": expected_alert}

        assert result["temperature"].value == expected_result["temperature"].value
        assert result["alert"] == expected_result["alert"]

    @pytest.mark.parametrize("temperature_list, expected_mean", [
        ([Temperature(25), Temperature(25), Temperature(25)], 25),
        ([Temperature(30), Temperature(20), Temperature(10), Temperature(40)], 25),
        ([Temperature(10), Temperature(20), Temperature(
            30), Temperature(40), Temperature(45)], 29)
    ])
    def test_check_mean_method(self, temperature_list, expected_mean):
        alert = TemperatureAlert(high_threshold=25, low_threshold=20)
        result = alert._get_mean(temperature_list)
        assert result.value == expected_mean
