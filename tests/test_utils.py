import datetime
import tempfile
import io
from experiencecloudapis.utils import (
    lower_keys,
    read_file_or_string,
    now_in_ms
)


def test_lower_keys():
    test_obj = {
        "A": "b",
        "C": {
            "d": "e"
        },
        "E": [1, 2, 3]
    }

    result = lower_keys(test_obj)
    assert list(result.keys()) == ["a", "c", "e"]


def test_read_file_or_string():
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(b"teststring")
    fp.close()
    str_1 = read_file_or_string(fp.name)
    f = io.StringIO()
    f.write("teststring")
    f.seek(0)
    str_2 = read_file_or_string(f)
    assert str_2 == "teststring"


def test_now_in_ms():
    date = datetime.datetime(2020, 1, 1)
    expected = 1577833200000
    assert now_in_ms(date) == expected
