import json
from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, Response, current_app, make_response

result_bp = Blueprint("result", __name__, url_prefix="/api")

@result_bp.route("/log/<uuid>", methods=['GET'])
def get_log(uuid):
    """
    這是一個回傳的 route function，主要拿來獲取某個評測 uuid 的 log。
    """
    LOG_FOLDER = current_app.config['LOG_FOLDER']
    file_path = f"{LOG_FOLDER}/{uuid}.json"
    
    try:
        with open(file_path, "r") as f:
            log_data = json.load(f)
    except Exception:
        return make_response({"error": "Failed to load log file"}, HTTPStatus.BAD_REQUEST)
    
    return make_response(log_data, HTTPStatus.OK)
