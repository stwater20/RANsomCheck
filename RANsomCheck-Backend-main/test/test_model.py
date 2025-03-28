from . import client
import time
import os
import json

from api.log import LogManager
from api.model_util import get_result
from api.model_service import upload_to_model, check_model_status, start_model_monitor

def test_get_result_success(client):
    tracker_id = "test"
    with client.application.app_context():
        prediction = get_result(tracker_id)
    assert prediction == [1.0] or prediction == [0.0]

def test_upload_to_model(client):
    tracker_id = "test_report"

    with client.application.app_context():
        result = upload_to_model(tracker_id)
    assert result == True

    # 檢查日誌文件是否存在
    log_path = os.path.join(client.application.config['LOG_FOLDER'], f"{tracker_id}.json")
    assert os.path.exists(log_path)
    
    # 檢查日誌內容
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
        assert log_data["current_status"] == "Completed"
        assert log_data["model_flow"]["success"] == True

def test_model_monitor(client):
    tracker_id = "test_report"

    with client.application.app_context():
        start_model_monitor(tracker_id)
    
    log_path = os.path.join(client.application.config['LOG_FOLDER'], f"{tracker_id}.json")
    assert os.path.exists(log_path)

    time.sleep(5)  # 等待一段時間以確保執行緒完成
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
        assert log_data["result"] != -1
