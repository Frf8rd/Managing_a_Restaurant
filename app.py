from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.dashboard import dashboard_bp
import os

app = Flask(__name__, template_folder="Frontend/html", static_folder="Frontend")
app.config.from_object(Config)

# Configurație UPLOAD_FOLDER - cale ABSOLUTĂ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crează folderul dacă nu există
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta specială pentru servirea fișierelor uploadate
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Configurare JWT
jwt = JWTManager(app)

# Înregistrare Blueprint-uri
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)

# Debugging - verifică căile
print(f"Current directory: {os.getcwd()}")
print(f"Base directory: {BASE_DIR}")
print(f"Upload folder: {UPLOAD_FOLDER}")
print(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
if os.path.exists(UPLOAD_FOLDER):
    print(f"Files in uploads: {os.listdir(UPLOAD_FOLDER)}")

if __name__ == "__main__":
    app.run(debug=True)