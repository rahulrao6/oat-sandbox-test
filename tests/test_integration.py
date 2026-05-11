"""Integration tests for the calculator web application."""

import json
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestCalculatorWorkflow:
    """Simulate realistic calculator usage sequences."""

    def _calc(self, client, a, b, op):
        resp = client.post(
            "/api/calculate",
            data=json.dumps({"a": a, "b": b, "operation": op}),
            content_type="application/json",
        )
        return resp.status_code, resp.get_json()

    def test_chained_operations(self, client):
        status, data = self._calc(client, 10, 5, "add")
        assert status == 200
        intermediate = data["result"]

        status, data = self._calc(client, intermediate, 3, "multiply")
        assert status == 200
        assert data["result"] == 45

    def test_all_operations_sequentially(self, client):
        status, data = self._calc(client, 100, 25, "add")
        assert status == 200
        assert data["result"] == 125

        status, data = self._calc(client, 100, 25, "subtract")
        assert status == 200
        assert data["result"] == 75

        status, data = self._calc(client, 100, 25, "multiply")
        assert status == 200
        assert data["result"] == 2500

        status, data = self._calc(client, 100, 25, "divide")
        assert status == 200
        assert data["result"] == pytest.approx(4.0)

    def test_error_then_valid_operation(self, client):
        status, data = self._calc(client, 5, 0, "divide")
        assert status == 400
        assert "error" in data

        status, data = self._calc(client, 5, 2, "multiply")
        assert status == 200
        assert data["result"] == 10

    def test_negative_numbers_workflow(self, client):
        status, data = self._calc(client, -10, -5, "add")
        assert status == 200
        assert data["result"] == -15

        status, data = self._calc(client, data["result"], -3, "divide")
        assert status == 200
        assert data["result"] == pytest.approx(5.0)

    def test_floating_point_workflow(self, client):
        status, data = self._calc(client, 0.1, 0.2, "add")
        assert status == 200
        assert data["result"] == pytest.approx(0.3)

        status, data = self._calc(client, data["result"], 3, "multiply")
        assert status == 200
        assert data["result"] == pytest.approx(0.9)

    def test_large_numbers(self, client):
        status, data = self._calc(client, 1_000_000, 2_000_000, "add")
        assert status == 200
        assert data["result"] == 3_000_000

        status, data = self._calc(client, data["result"], 3, "divide")
        assert status == 200
        assert data["result"] == pytest.approx(1_000_000)

    def test_response_structure(self, client):
        status, data = self._calc(client, 2, 3, "add")
        assert status == 200
        assert "result" in data
        assert "error" not in data

    def test_error_response_structure(self, client):
        status, data = self._calc(client, 2, 0, "divide")
        assert status == 400
        assert "error" in data
        assert "result" not in data

    def test_index_page_serves_html_with_buttons(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        content = resp.data.decode("utf-8")
        for digit in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            assert f'data-digit="{digit}"' in content
        for op in ["add", "subtract", "multiply", "divide"]:
            assert f'data-op="{op}"' in content

    def test_404_for_unknown_route(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404

    def test_method_not_allowed_get_on_calculate(self, client):
        resp = client.get("/api/calculate")
        assert resp.status_code == 405
