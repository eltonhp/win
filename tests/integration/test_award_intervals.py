import os

import requests

BASE_URL = os.getenv("API_BASE_URL", "http://win:8081")

def test_award_intervals_data_types_are_correct():
    url = f"{BASE_URL}/award-intervals"
    response = requests.post(url)
    data = response.json()

    for group in ["min", "max"]:
        for item in data[group]:
            assert isinstance(item["producer"], str)
            assert isinstance(item["interval"], int)
            assert isinstance(item["previousWin"], int)
            assert isinstance(item["followingWin"], int)


def test_award_intervals_contains_expected_keys_and_fields():
    url = f"{BASE_URL}/award-intervals"
    response = requests.post(url)
    data = response.json()

    assert "min" in data and "max" in data

    for group in ["min", "max"]:
        for entry in data[group]:
            assert "producer" in entry
            assert "interval" in entry
            assert "previousWin" in entry
            assert "followingWin" in entry

def test_award_intervals_returns_expected_result():
    url = f"{BASE_URL}/award-intervals"
    response = requests.post(url)

    assert response.status_code == 200

    expected = {
        "min": [
            {
                "producer": "Joel Silver",
                "interval": 1,
                "previousWin": 1990,
                "followingWin": 1991
            }
        ],
        "max": [
            {
                "producer": "Matthew Vaughn",
                "interval": 13,
                "previousWin": 2002,
                "followingWin": 2015
            }
        ]
    }

    assert response.json() == expected