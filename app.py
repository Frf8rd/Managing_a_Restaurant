from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__, template_folder="Frontend/html", static_folder="Frontend")
app.config.from_object(Config)

# Configurare JWT
jwt = JWTManager(app)

# Înregistrare Blueprint-uri
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
