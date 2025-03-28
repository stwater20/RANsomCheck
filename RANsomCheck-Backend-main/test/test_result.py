from . import client

import json
from http import HTTPStatus
from pathlib import Path

def test_get_log_success(client):
    test_uuid = 'abcd-1234'
    test_log_data = {"status": "success"}
    
    log_file_path = Path(client.application.config['LOG_FOLDER']) / f"{test_uuid}.json"
    with open(log_file_path, 'w') as f:
        json.dump(test_log_data, f)
    
    response = client.get(f'/log/{test_uuid}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == test_log_data

def test_get_log_file_not_found(client):
    test_uuid = 'non-existent-log'
    
    response = client.get(f'/log/{test_uuid}')
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"error": "Failed to load log file"}
