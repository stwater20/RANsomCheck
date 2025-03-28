import os
import json
from datetime import datetime
from flask import current_app

class LogManager:
    def __init__(self, tracker_id):
        # 使用 current_app 獲取 LOG_FOLDER 配置
        LOG_FOLDER = current_app.config['LOG_FOLDER']
        
        self.file_name = tracker_id
        self.log_path = os.path.join(LOG_FOLDER, f"{self.file_name}.json")

        if os.path.exists(self.log_path):
            self.log_data = self.load_log()
        else:
            self.log_data = self.create_log()

    def create_log(self):
        """創建日誌文件並返回初始的 log_data"""
        log_data = {
            "file_name": self.file_name,
            "tracker_id": self.file_name,
            "current_status": "initializing",
            "upload_flow": {
                "start_time": "",
                "end_time": "",
                "success": False
            },
            "task_id": 0,
            "SHA256":"",
            "API calls":[],
            "cuckoo_flow": {
                "start_time": "",
                "analysis_time": "",
                "end_time": "",
                "success": False
            },
            "model_flow": {
                "start_time": "",
                "end_time": "",
                "success": False
            },
            "result": -1,
            "error_message": ""
        }

        try:
            with open(self.log_path, 'w') as log_file:
                json.dump(log_data, log_file, indent=4)
            return log_data
        except Exception as e:
            print(f"Error creating log file: {e}")
            return None

    def load_log(self):
        """載入已存在的日誌文件"""
        try:
            with open(self.log_path, 'r') as log_file:
                return json.load(log_file)
        except json.JSONDecodeError:
            print(f"Error: Corrupted log file at {self.log_path}. Recreating log.")
            return self.create_log()
        except Exception as e:
            print(f"Error loading log file: {e}")
            return None

    def update_log_stage(self, current_stage, additional_data=None):
        if not os.path.exists(self.log_path):
            self.log_data = self.create_log()
        else:
            self.log_data = self.load_log()

        self.log_data["current_status"] = current_stage

        if additional_data and isinstance(additional_data, dict):
            for key, value in additional_data.items():
                if key in self.log_data:
                    if isinstance(self.log_data[key], dict) and isinstance(value, dict):
                        self.log_data[key].update(value)
                    else:
                        self.log_data[key] = value
                else:
                    print(f"Warning: Key '{key}' not found in log structure.")
        else:
            if additional_data:
                print(f"Warning: additional_data should be a dictionary but got {type(additional_data)}.")

        try:
            with open(self.log_path, 'w') as log_file:
                json.dump(self.log_data, log_file, indent=4)
        except Exception as e:
            print(f"Error writing to log file: {e}")
