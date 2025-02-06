
import pytest
from model.enum_alerts import EnumAlerts


class TestEnumAlerts():
    @pytest.mark.parametrize("alert", ["Normal temperature"])
    def test_normal_alert(self, alert):
        assert EnumAlerts.NORMAL.value == alert

    @pytest.mark.parametrize("alert", ["High temperature"])
    def test_high_alert(self, alert):
        assert EnumAlerts.HIGH.value == alert

    @pytest.mark.parametrize("alert", ["Low temperature"])
    def test_low_alert(self, alert):
        assert EnumAlerts.LOW.value == alert
