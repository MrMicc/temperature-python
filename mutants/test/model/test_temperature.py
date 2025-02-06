import pytest
from src.model.temperature import Temperature


class TestTemperature():

    @pytest.mark.parametrize("temperature", [25.5])
    def test_create_temperature(self, temperature):
        result = Temperature(temperature)
        expected = temperature
        assert result.value == expected

    @pytest.mark.parametrize("value", [-100, 45.1, -10.1, 100])
    def test_invalid_temperature(self, value):
        with pytest.raises(ValueError):
            Temperature(value)
