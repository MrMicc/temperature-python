import pytest
from datetime import datetime, timezone
from model.temperature import Temperature


class TestTemperature():

    @pytest.mark.parametrize("temperature", [25.5, 45, -10])
    def test_create_temperature(self, temperature):
        result = Temperature(temperature)
        expected = temperature
        assert result.value == expected

    @pytest.mark.parametrize("value", [-100, 45.1, -10.1, 100])
    def test_invalid_temperature(self, value):
        with pytest.raises(ValueError):
            Temperature(value)

    @pytest.mark.parametrize("temperature", [25.5, 45, -10])
    def test_check_time_is_datetime(self, temperature):
        result = Temperature(temperature)
        result_time = result.timestamp
        assert isinstance(result_time, datetime)

    @pytest.mark.parametrize("temperature", [25.5, 45, -10])
    def test_time_is_created(self, temperature):
        result = Temperature(temperature)
        result_time = result.timestamp
        expected_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        assert result_time.strftime("%Y-%m-%d %H:%M") == expected_time
