import pytest
from datetime import datetime,  timezone
import time
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

    def test_time_created_id_attribute(self):
        result = Temperature(25.5)
        expected_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        assert result.id == expected_id

    def test_timestamp_changes_on_new_instace(self):
        temp1 = Temperature(25.5)
        time.sleep(1)
        temp2 = Temperature(25.5)
        assert temp1.timestamp < temp2.timestamp
