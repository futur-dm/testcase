import io
import json
import tempfile
import os

import pytest

from script import read_logs, average


@pytest.fixture
def test_log_lines():
    return [
        {"@timestamp": "2025-06-22T13:59:37+00:00", "status": 200, "url": "/api/test_url_1", "request_method": "GET", "response_time": 0.1, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:59:38+00:00", "status": 200, "url": "/api/test_url_1", "request_method": "GET", "response_time": 0.2, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:59:39+00:00", "status": 200, "url": "/api/test_url_2", "request_method": "GET", "response_time": 0.4, "http_user_agent": "..."},
        {"@timestamp": "2025-06-22T13:59:40+00:00", "status": 200, "url": "/api/test_url_1", "request_method": "GET", "response_time": 0.3, "http_user_agent": "..."},
    ]

@pytest.fixture
def test_log_file(test_log_lines):
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as f:
        for entry in test_log_lines:
            f.write(json.dumps(entry) + '\n')
        fname = f.name
    yield fname
    os.remove(fname)

def test_logs(test_log_file):
    endpoints = read_logs([test_log_file])

    assert "/api/test_url_1" in endpoints
    assert "/api/test_url_1" in endpoints

    assert endpoints["/api/test_url_1"]["count"] == 3
    assert endpoints["/api/test_url_1"]["total_time"] == pytest.approx(0.6)
    assert endpoints["/api/test_url_2"]["count"] == 1
    assert endpoints["/api/test_url_2"]["total_time"] == pytest.approx(0.4)

def test_average(test_log_file):
    endpoints = read_logs([test_log_file])
    report = average(endpoints)

    test_url_1_row = next(row for row in report if row[0] == "/api/test_url_1")
    bar_row = next(row for row in report if row[0] == "/api/test_url_2")

    assert test_url_1_row[1] == 3
    assert test_url_1_row[2] == pytest.approx(0.2)
    assert bar_row[1] == 1
    assert bar_row[2] == pytest.approx(0.4)
