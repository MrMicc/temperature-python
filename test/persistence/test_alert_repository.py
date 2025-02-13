from enum import Enum
import pytest
from model.enum_alerts import EnumAlerts
from model.temperature import Temperature
from persistence.alert_repository import SqliteAlertRepository


class TestAlertRepository():

    @pytest.fixture
    def db_connection(self, tmp_path):
        path = tmp_path / "test_temperature.db"
        connection = SqliteAlertRepository(path)
        return connection

    def test_save_alert(self, db_connection):
        repository = db_connection
        temperature = Temperature(25.5)
        alert = EnumAlerts.HIGH

        expected = {"temperature": temperature, "alert": alert}

        saved_alert = repository.save(temperature=temperature, alert=alert)
        assert saved_alert["temperature"].value == expected["temperature"].value
        assert saved_alert["alert"] == expected["alert"]

    def test_get_last_alert(self, db_connection):
        repository = db_connection
        temperature = Temperature(25.5)
        alert = EnumAlerts.NORMAL

        expected = {"temperature": temperature, "alert": alert}

        repository.save(temperature=temperature, alert=alert)
        saved_alert = repository.get_last_alert()

        assert saved_alert["temperature"].value == expected["temperature"].value
        assert saved_alert["alert"] == expected["alert"]

    def test_get_last_alert_with_no_alert(self, db_connection):
        repository = db_connection

        expected = {"temperature": None, "alert": None}

        saved_alert = repository.get_last_alert()

        assert saved_alert["temperature"] == expected["temperature"]
        assert saved_alert["alert"] == expected["alert"]
