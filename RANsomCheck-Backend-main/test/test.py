from . import client

import os
from http import HTTPStatus
from io import BytesIO

# def test_upload_file_success_ori(client):
#     # 上傳文件的模擬
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     test_file_path = os.path.join(base_dir, 'test_data', 'dist', 'test.exe')
#     with open(test_file_path, 'rb') as test_file:
#         data = {
#             'file': (BytesIO(test_file.read()), 'test.exe')
#         }

#     # 發送 POST 請求上傳文件
#     response = client.post('/upload', data=data, content_type='multipart/form-data')

#     json_data = response.get_json()

#     # 確認 HTTP 請求成功
#     # assert response.status_code == HTTPStatus.OK
#     tracker_id = json_data["tracker_id"]
#     assert json_data["message"] == f"File {tracker_id} uploaded successfully."

#     # 獲取回應中的 tracker_id
#     response_data = response.get_json()
#     tracker_id = response_data.get('tracker_id')

#     # 檢查檔案是否上傳成功到指定目錄
#     uploaded_file_path = os.path.join(client.application.config['UPLOAD_FOLDER'], 'test.exe')
#     assert os.path.exists(uploaded_file_path)

#     # 檢查是否生成了對應的 log 文件
#     log_file_path = os.path.join(client.application.config['LOG_FOLDER'], f'{tracker_id}.json')
#     print(client.application.config['LOG_FOLDER'])
#     assert os.path.exists(log_file_path)

#     # 測試完成後清理檔案
#     # os.remove(uploaded_file_path)
#     # os.remove(log_file_path)

# from . import client

# import os
# from http import HTTPStatus
# from io import BytesIO

def test_upload_file_success(client):
    # 上傳文件的模擬
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(base_dir, 'test_data', 'dist', 'test.exe')
    with open(test_file_path, 'rb') as test_file:
        data = {
            'file': (BytesIO(test_file.read()), 'test.exe')
        }

    # 發送 POST 請求上傳文件
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    json_data = response.get_json()

    # 確認 HTTP 請求成功
    assert response.status_code == HTTPStatus.OK
    tracker_id = json_data["tracker_id"]
    assert json_data["message"] == f"File {tracker_id} uploaded successfully."

    # 檢查 start_cuckoo_monitor 是否被呼叫
    # mock_monitor.assert_called_once_with()

    # 檢查檔案是否上傳成功到指定目錄
    uploaded_file_path = os.path.join(client.application.config['UPLOAD_FOLDER'], 'test.exe')
    assert os.path.exists(uploaded_file_path)

    # 檢查是否生成了對應的 log 文件
    log_file_path = os.path.join(client.application.config['LOG_FOLDER'], f'{tracker_id}.json')
    assert os.path.exists(log_file_path)

    # 測試完成後清理檔案
    # os.remove(uploaded_file_path)
    # os.remove(log_file_path)
