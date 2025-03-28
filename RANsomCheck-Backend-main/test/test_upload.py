from . import client

import io
import os
import pytest
from io import BytesIO
from tempfile import NamedTemporaryFile

def test_upload_no_file_part(client):
    response = client.post('/upload', data={})
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['error'] == 'No file part.'

def test_upload_no_selected_file(client):
    data = {'file': (BytesIO(b''), '')}
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['error'] == 'No selected file.'

def test_upload_wrong_file(client):
    data = {
        'file': (BytesIO(b'test file content'), 'testfile.txt')
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    json_data = response.get_json()
    
    assert response.status_code == 400
    assert json_data['message'] == 'Wrong type of file.'

def test_valid_exe_upload(client):
    with NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
        temp_file.write(b'test file content')
        temp_file.seek(0)
        file_path = temp_file.name

        data = {
            'file': (open(file_path, 'rb'), os.path.basename(file_path))
        }

        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200

    os.remove(file_path)
