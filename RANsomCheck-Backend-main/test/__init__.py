import os
import pytest
from app import create_app

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.config['LOG_FOLDER'] = 'test_logs'
    app.config['REPORT_FOLDER'] = 'test_reports'
    
    with app.test_client() as client:
        with app.app_context():
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
            os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
        yield client
