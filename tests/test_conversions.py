import base64, re, pytest

# Correct little-endian base64 reference (what the spec requires)
def int_to_b64_le(n: int) -> str:
    length = max(1, (n.bit_length() + 7) // 8)
    return base64.b64encode(n.to_bytes(length, "little")).decode("ascii")

def norm_hex(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"^0x", "", s)
    return s.lstrip("0") or "0"

def norm_bin(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"^0b", "", s)
    s = s.lstrip("0") or "0"
    if not set(s) <= {"0", "1"}:
        raise AssertionError("non-binary chars")
    return s

def fmt_ui(n: int, t: str) -> str:
    t = t.lower()
    if t == "decimal": return str(n)
    if t == "hexadecimal": return format(n, "x")
    if t == "binary": return format(n, "b")
    if t == "octal": return format(n, "o")
    if t == "base64": return int_to_b64_le(n)
    raise AssertionError(f"bad type: {t}")

def norm_out(t: str, s: str) -> str:
    t = t.lower()
    if t == "hexadecimal": return norm_hex(s)
    if t == "binary": return norm_bin(s)
    if t == "decimal": return str(int(s))
    return s.strip().lower()

UI_TYPES = ["decimal", "hexadecimal", "binary", "octal", "base64"]
INTS = [0,1,2,7,8,15,16,31,32,42,255,256,65535,1048576,2**31-1]

@pytest.mark.parametrize("n", INTS)
@pytest.mark.parametrize("to_t", UI_TYPES)
@pytest.mark.parametrize("from_t", UI_TYPES)
def test_matrix_via_http(call_convert, n, from_t, to_t):
    src = fmt_ui(n, from_t)
    data = call_convert(src, from_t, to_t)
    assert "result" in data and "error" in data
    assert data["error"] in (None, ""), f"unexpected error: {data}"
    out = data["result"]
    exp = fmt_ui(n, to_t)
    assert norm_out(to_t, out) == norm_out(to_t, exp)

def test_base64_endianness_specifics(call_convert):
    # These intentionally FAIL until index.py is fixed to little-endian.
    cases = {
        "256": "AAE=",
        "1048576": "AAAQ",
        str(2**31 - 1): "////fw==",
    }
    for dec, expected_b64 in cases.items():
        data = call_convert(dec, "decimal", "base64")
        assert data["error"] in (None, ""), f"unexpected error: {data}"
        assert data["result"] == expected_b64, f"Expected little-endian for {dec}"
    
def test_base64_roundtrip_identity(call_convert):
    """
    A base64 string should round-trip back to itself when
    converted base64 -> base64.
    """
    # Noticed that the round trip from "AA==" to "AA==" was failing instead "AQ==" is returned
    samples = ["AA==", "AQ==", "/w==", "AAE=", "//8="]
    for b64 in samples:
        data = call_convert(b64, "base64", "base64")
        assert data["error"] in (None, "")
        assert data["result"] == b64, f"base64 round-trip failed for {b64}"

