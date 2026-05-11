"""Unit tests for the Flask API endpoints."""

import json
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestIndexRoute:
    def test_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_returns_html(self, client):
        resp = client.get("/")
        assert b"calculator" in resp.data.lower() or b"Calculator" in resp.data


class TestCalculateEndpoint:
    def _post(self, client, payload):
        return client.post(
            "/api/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_add(self, client):
        resp = self._post(client, {"a": 3, "b": 4, "operation": "add"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == 7

    def test_subtract(self, client):
        resp = self._post(client, {"a": 10, "b": 4, "operation": "subtract"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == 6

    def test_multiply(self, client):
        resp = self._post(client, {"a": 3, "b": 7, "operation": "multiply"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == 21

    def test_divide(self, client):
        resp = self._post(client, {"a": 10, "b": 4, "operation": "divide"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(2.5)

    def test_divide_by_zero(self, client):
        resp = self._post(client, {"a": 5, "b": 0, "operation": "divide"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()
        assert "zero" in resp.get_json()["error"].lower()

    def test_missing_operand_a(self, client):
        resp = self._post(client, {"b": 4, "operation": "add"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_missing_operand_b(self, client):
        resp = self._post(client, {"a": 4, "operation": "add"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_missing_operation(self, client):
        resp = self._post(client, {"a": 4, "b": 2})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_unknown_operation(self, client):
        resp = self._post(client, {"a": 4, "b": 2, "operation": "power"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_non_numeric_operands(self, client):
        resp = self._post(client, {"a": "abc", "b": 2, "operation": "add"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_float_operands(self, client):
        resp = self._post(client, {"a": 1.5, "b": 2.5, "operation": "add"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == pytest.approx(4.0)

    def test_negative_operands(self, client):
        resp = self._post(client, {"a": -5, "b": 3, "operation": "add"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == -2

    def test_no_json_body(self, client):
        resp = client.post("/api/calculate", data="not json", content_type="text/plain")
        assert resp.status_code in (400, 415)

    def test_string_numeric_operands(self, client):
        resp = self._post(client, {"a": "3", "b": "4", "operation": "multiply"})
        assert resp.status_code == 200
        assert resp.get_json()["result"] == 12
