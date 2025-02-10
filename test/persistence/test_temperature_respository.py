import pytest
import sqlite3
from unittest.mock import MagicMock
from datetime import datetime
from model.temperature import Temperature
from errors.custom_errors import NoDataFoundError

from persistence.temperature_repository import SqliteTemperatureRepository, TemperatureRepository


class TestTemperatureRepository():

    @pytest.fixture
    def db_connection(self, tmp_path):
        db_path = tmp_path / "test_temperature.db"
        return db_path

    @pytest.mark.parametrize("expected_value", [25.5, 45, -10])
    def test_save_temperature(self, db_connection, expected_value):
        temperature_repository = SqliteTemperatureRepository(db_connection)
        temperature = Temperature(expected_value)

        temperature_repository.save(temperature)

        sqlite_connection = sqlite3.connect(db_connection)
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT id, value, timestamp FROM temperature")
        result = cursor.fetchone()

        expected_id = temperature.timestamp.strftime("%Y%m%d%H%M%S")
        assert result[0] == expected_id
        assert result[1] == temperature.value
        assert isinstance(result[2], str)
        assert isinstance(datetime.fromisoformat(result[2]), datetime)

    def test_get_last_temperature(self, db_connection):
        temperature_repository = SqliteTemperatureRepository(db_connection)
        temperature_repository.save(Temperature(25.5))
        temperature_repository.save(Temperature(45))
        temperature_repository.save(Temperature(-10))

        result = temperature_repository.get_last_temperature()

        assert result.value == -10

    def test_get_last_temperature_no_data(self, db_connection):
        temperature_repository = SqliteTemperatureRepository(db_connection)

        with pytest.raises(NoDataFoundError):
            temperature_repository.get_last_temperature()
