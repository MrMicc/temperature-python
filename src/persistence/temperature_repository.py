from abc import ABC, abstractmethod
import sqlite3
from model.temperature import Temperature
from errors.custom_errors import NoDataFoundError


class TemperatureRepository(ABC):
    @abstractmethod
    def save(self, temperature: Temperature):
        raise NotImplementedError

    @abstractmethod
    def get_last_temperature(self) -> Temperature:
        raise NotImplementedError

    @abstractmethod
    def get_temperature_list(self, list_size=20) -> list[Temperature]:
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

    def get_temperature_list(self, list_size=20) -> list[Temperature]:
        with self.db_connection as connection:
            query = f"SELECT value, timestamp FROM temperature ORDER BY timestamp DESC LIMIT {list_size}"
            cursor = connection.execute(query)
            result = cursor.fetchall()
            return [Temperature(row[0], row[1]) for row in result]
