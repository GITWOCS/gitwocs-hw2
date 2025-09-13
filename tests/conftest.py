import sys, pathlib, importlib
import pytest

# Ensure repo root is on sys.path so `import api.index` works
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session")
def app():
    mod = importlib.import_module("api.index")  # loads your Flask app
    mod.app.testing = True
    return mod.app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def call_convert(client):
    """Callable that POSTs to /convert and returns the JSON payload."""
    def _call(value: str, input_type: str, output_type: str):
        resp = client.post(
            "/convert",
            json={"input": value, "inputType": input_type, "outputType": output_type},
        )
        assert resp.status_code == 200, f"HTTP {resp.status_code} on /convert"
        return resp.get_json()
    return _call
