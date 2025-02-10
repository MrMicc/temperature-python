from abc import ABC
import sqlite3
from model.temperature import Temperature
from errors.custom_errors import NoDataFoundError


class TemperatureRepository(ABC):
    def save(self, temperature: Temperature):
        raise NotImplementedError

    def get_last_temperature(self) -> Temperature:
        raise NotImplementedError


class SqliteTemperatureRepository(TemperatureRepository):
    def __init__(self, connection_path: str):
        self.db_connection = sqlite3.connect(connection_path)
        self._init_db()

    def _init_db(self):
        with self.db_connection as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS temperature (id, value float, timestamp datetime)")
            connection.execute(
                "CREATE INDEX IF NOT EXISTS timestamp_index ON temperature(timestamp)")
            connection.execute(
                "CREATE INDEX IF NOT EXISTS id_index ON temperature(id)")
            connection.commit()

    def save(self, temperature: Temperature):
        with self.db_connection as connection:
            query = "INSERT INTO temperature (id, value, timestamp) VALUES (?, ?, ?) "
            connection.execute(
                query,
                (temperature.id, temperature.value, temperature.timestamp.isoformat()))
            connection.commit()

    def get_last_temperature(self) -> Temperature:
        with self.db_connection as connection:
            query = "SELECT value, timestamp FROM temperature ORDER BY timestamp DESC LIMIT 1"
            cursor = connection.execute(query)

            row = cursor.fetchone()

            if row is None:
                raise NoDataFoundError("NO DATA FOUND: "+query)
            return Temperature(row[0], row[1])
