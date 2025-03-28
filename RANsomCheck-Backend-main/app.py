import os

from flask import Flask

from api.upload_route import upload_bp
from api.result_route import result_bp

def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = 'uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.config['LOG_FOLDER'] = 'logs'
    if not os.path.exists(app.config['LOG_FOLDER']):
        os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)

    app.config['REPORT_FOLDER'] = 'reports'
    if not os.path.exists(app.config['REPORT_FOLDER']):
        os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

    app.config['ALLOWED_MIME_MAGIC'] = {b'MZ'}
    app.config['ALLOWED_EXTENSIONS'] = {'exe', 'dll'}

    app.register_blueprint(upload_bp)
    app.register_blueprint(result_bp)
    
    return app