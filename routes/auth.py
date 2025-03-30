from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token
import bcrypt
from database import get_connection

auth_bp = Blueprint('auth', __name__)

ALLOWED_ADMIN_EMAILS = ['admin@example.com']

@auth_bp.route('/')
def auth():
    return render_template('auth.html')

@auth_bp.route('/register', methods=['POST'])
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

    return jsonify({'message': 'Înregistrare reușită', 'redirect': '/dashboard'}), 201

@auth_bp.route('/login', methods=['POST'])
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
    return jsonify({
        'message': 'Autentificare reușită!',
        'redirect': '/dashboard',
        'access_token': access_token,
        'username': user[0],
        'role': user[3]
    }), 200
