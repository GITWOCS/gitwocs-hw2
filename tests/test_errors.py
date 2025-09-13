import pytest

@pytest.mark.parametrize("value,ft,tt", [
    ("0xG1", "hexadecimal", "decimal"),  # invalid hex
    ("21010", "binary", "decimal"),      # invalid binary
    ("!!!", "base64", "decimal"),        # invalid base64
    ("42", "weird", "decimal"),          # unknown input type
    ("42", "decimal", "weird"),          # unknown output type
])
def test_error_cases_via_http(call_convert, value, ft, tt):
    data = call_convert(value, ft, tt)
    # Flask handler returns 200 with an error string on failure
    assert data["error"] not in (None, ""), f"expected error for {ft}->{tt}, got: {data}"
