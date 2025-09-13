import re

def _flat(s: str) -> str:
    return re.sub(r"[\s-]+", "", s.lower())

def test_decimal_to_binary(call_convert):
    data = call_convert("42", "decimal", "binary")
    assert data["error"] in (None, "")
    assert data["result"] == "101010"

def test_text_to_decimal(call_convert):
    data = call_convert("forty two", "text", "decimal")
    assert data["error"] in (None, "")
    assert data["result"] == "42"

def test_hex_to_text(call_convert):
    data = call_convert("2a", "hexadecimal", "text")
    assert data["error"] in (None, "")
    assert _flat(data["result"]) == "fortytwo"
