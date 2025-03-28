from . import client

import os
import json
import pytest
import tempfile
import shutil

from flask import current_app
from http import HTTPStatus

TEST_UUID = "test-uuid"
LOG_FOLDER = "test_logs"
LOG_FILE_PATH = f"{LOG_FOLDER}/{TEST_UUID}.json"

def create_test_log_file():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    with open(LOG_FILE_PATH, "w") as f:
        json.dump({"test": "log content"}, f)

def test_get_log_success(client):
    create_test_log_file()

    response = client.get(f"/log/{TEST_UUID}")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"test": "log content"}