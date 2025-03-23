from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
from database import get_connection

app = Flask(__name__, template_folder="Frontend/html", static_folder="Frontend")

# Configurare JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Schimbă cu o cheie puternică
jwt = JWTManager(app)

# Lista de email-uri pentru administratori (sau poți face o verificare în DB)
ALLOWED_ADMIN_EMAILS = ['admin@example.com']

# # Ruta principală - afișează meniul din DB
# @app.route("/")
# def home():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM menu")
#     rezultate = cursor.fetchall()
#     conn.close()
#     return render_template("index.html", date=rezultate)

# Pagina de autentificare/înregistrare (aceeași pentru ambele)
@app.route("/")
def auth():
    return render_template('auth.html')

# Înregistrare utilizator
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email și password sunt necesare'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user:
        conn.close()
        return jsonify({'message': 'Email deja înregistrat'}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    role = 'admin' if email in ALLOWED_ADMIN_EMAILS else 'user'

    cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                   (username, email, password_hash.decode('utf-8'), role))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Utilizator înregistrat cu succes', 'role': role}), 201

# Autentificare utilizator
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email și parola sunt necesare'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, password_hash, role FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'message': 'Email sau parolă incorectă'}), 401

    access_token = create_access_token(identity={'username': user[0], 'email': user[1], 'role': user[3]})
    return jsonify({'access_token': access_token, 'username': user[0], 'role': user[3]}), 200

# Endpoint protejat pentru administratori
@app.route('/admin-only', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Acces interzis. Nu ești admin!'}), 403
    return jsonify({'message': f'Bun venit, {current_user["username"]} (Admin)!'}), 200

if __name__ == "__main__":
    app.run(debug=True)
