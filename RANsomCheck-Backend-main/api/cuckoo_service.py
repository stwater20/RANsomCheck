import requests
import threading
import time
import os
import json

from tempfile import NamedTemporaryFile
from requests.exceptions import Timeout
from datetime import datetime
from http import HTTPStatus
from dotenv import load_dotenv

from flask import current_app

from .FlaskThread import FlaskThread
from .log import LogManager
from .model_service import start_model_monitor, upload_to_model

CUCKOO_URL = 'http://140.124.181.155'
PORT = '1337'
load_dotenv() 
HEADERS = os.getenv('HEADERS')
HEADERS = json.loads(HEADERS) 

def upload_to_cuckoo(tracker_id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    LOG_FOLDER = current_app.config['LOG_FOLDER']

    log_manager = LogManager(tracker_id)

    additional_data = {
        "cuckoo_flow": {
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    log_manager.update_log_stage("Cuckoo uploaded", additional_data)

    try:
        log_path = os.path.join(LOG_FOLDER, f"{tracker_id}.json")
        file_name = ""
        with open(log_path, 'r') as log_file:
            data = json.load(log_file)
            file_name = data["file_name"]
        path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(path, "rb") as sample:
            files = {"file": ("files", sample), "priority": 4, "unique": False}
            r = requests.post(CUCKOO_URL + ":" + str(PORT) +  '/tasks/create/file', files=files, headers=HEADERS, timeout=30, data={"priority": 4, "unique": False})

        if(r.status_code != HTTPStatus.OK):
            return False, "Upload failed."
        else:
            task_id = r.json()["task_id"]
            additional_data = {
                "task_id": task_id
            }
            log_manager.update_log_stage("Cuckoo uploaded", additional_data)
            return True, task_id
        
    except Timeout:
        return False, "Connection timed out."

def start_cuckoo_monitor(tracker_id):
    print("start monitor")
    with current_app.app_context():
        log_manager = LogManager(tracker_id)
        log_manager.update_log_stage("Cuckoo monitor started")

    app = current_app._get_current_object()

    thread = FlaskThread(
        app = app,
        target=check_cuckoo_status_with_context,
        kwargs={"tracker_id": tracker_id, "app": app}
    )
    thread.start()

def check_cuckoo_status_with_context(tracker_id, app):
    with app.app_context():
        check_cuckoo_status(tracker_id)

def check_cuckoo_status(tracker_id):
    with current_app.app_context():
        log_manager = LogManager(tracker_id)
        LOG_FOLDER = current_app.config['LOG_FOLDER']

        try:
            log_path = os.path.join(LOG_FOLDER, f"{tracker_id}.json")
            with open(log_path, 'r') as log_file:
                data = json.load(log_file)
                task_id = data["task_id"]
        except FileNotFoundError:
            print("filed")
            return False, "Doesn't find log file."
        
        start_analyzing = False
        while True:
            time.sleep(10)

            r = requests.get(CUCKOO_URL + ":" + str(PORT) + '/tasks/view/' + str(task_id), headers=HEADERS)
            
            status = r.json()["task"]["status"]
            print(status)

            if(r.status_code == HTTPStatus.OK and status == "reported"):
                success = download_report(tracker_id, task_id)
                if(success):
                    additional_data = {
                        "cuckoo_flow": {
                            "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "success": True
                        }
                    }
                    log_manager.update_log_stage("Cuckoo completed", additional_data)
                    
                    upload_to_model(tracker_id)
                    start_model_monitor(tracker_id)
                    return True, "cuckoo success."
                else:
                    additional_data = {
                        "cuckoo_flow": {
                            "success": False
                        },
                        "error_message": "can not download the cuckoo report."
                    }
                    log_manager.update_log_stage("Cuckoo completed", additional_data)
                    return False, "Cuckoo failed."
            elif(r.status_code == HTTPStatus.OK and status == "running"):
                if start_analyzing:
                    continue
                additional_data = {
                    "cuckoo_flow": {
                        "analysis_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                log_manager.update_log_stage("Cuckoo analyzing", additional_data)
                start_analyzing = True
            elif(r.status_code == 404):
                additional_data = {
                    "cuckoo_flow": {
                        "complete_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "success": False
                    },
                    "error_message": "cuckoo analyze failed."
                }
                log_manager.update_log_stage("Failed", additional_data)
                return False, "Cuckoo failed"

def download_report(tracker_id, task_id):
    REPORT_FOLDER = current_app.config['REPORT_FOLDER']

    success, result = fetch_result_by_ID(task_id)
    
    if success:
        file_path = os.path.join(REPORT_FOLDER, f"{tracker_id}.json")
        with open(file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(json.dumps(result, ensure_ascii=False, indent=4))

        additional_data = {
            "SHA256": result["target"]["file"]["sha256"]
        }
        with current_app.app_context():
            log_manager = LogManager(tracker_id)
            log_manager.update_log_stage("Cuckoo completed", additional_data)
        return True
    
    additional_data = {
        "error_message": "Download report failed"
    }
    with current_app.app_context():
        log_manager = LogManager(tracker_id)
        log_manager.update_log_stage("Failed", additional_data)
    return False

def fetch_result_by_ID(id):
    r = requests.get(CUCKOO_URL + ":" + str(PORT) +  '/tasks/report/' + str(id) + '/json', headers=HEADERS)
    print(r.status_code)
    if(r.status_code == 200):
        result = r.json()
        return True, result
    elif(r.status_code == 400):
        return False, "Invalid report format."
    elif(r.status_code == 404):
        return False, "Report not found."
    else:
        return False, "Unknown error."

