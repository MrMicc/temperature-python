from abc import ABC, abstractmethod
import sqlite3
from model.temperature import Temperature
from model.enum_alerts import EnumAlerts


class AlertRepository(ABC):

    def __init__(self, db_connection):
        self.db_connection = db_connection

    @abstractmethod
    def save(self, temperature: Temperature, alert: EnumAlerts):
        raise NotImplementedError


class SqliteAlertRepository(AlertRepository):
    def __init__(self, connection_path: str):
        self.db_connection = sqlite3.connect(connection_path)
        self._init_db()

    def _init_db(self):
        with self.db_connection as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS temperature_alert (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature FLOAT,
                    alert TEXT NOT NULL,
                    timestamp )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS timestamp_index ON temperature_alert(timestamp)")
            connection.execute(
                "CREATE INDEX IF NOT EXISTS id_index ON temperature_alert(id)")
            connection.commit()

    def save(self, temperature: Temperature, alert: EnumAlerts) -> dict:
        with self.db_connection as connection:
            query = "INSERT INTO temperature_alert (temperature, alert, timestamp) VALUES (?, ?, ?) "
            connection.execute(
                query, (temperature.value, alert.value, temperature.timestamp.isoformat()))
            connection.commit()
        return {"temperature": temperature, "alert": alert}

    def get_last_alert(self) -> dict:
        with self.db_connection as connection:
            query = "SELECT id, temperature, alert FROM temperature_alert ORDER BY timestamp DESC LIMIT 1"
            cursor = connection.execute(query)
            result = cursor.fetchone()
            if result:
                return {"temperature": Temperature(value=result[1], id=result[0]), "alert": EnumAlerts(result[2])}
        return {"temperature": None, "alert": None}
