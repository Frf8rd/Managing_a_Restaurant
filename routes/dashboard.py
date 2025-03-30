from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':  # Adăugare produs
        data = request.json
        available = data.get('available', True)  # Valoare implicită True dacă nu e specificată
        
        cursor.execute("INSERT INTO menu_items (name, description, price, available, image_url) VALUES (%s, %s, %s, %s, %s)", 
                    (data['name'], data['description'], data['price'], available, data['image_url']))
        conn.commit()
        
        # Obținem ID-ul produsului nou adăugat
        new_id = cursor.lastrowid
        
        return jsonify({
            "message": "Item added successfully",
            "id": new_id
        }), 201

    if request.method == 'PUT':  # Actualizare produs
        data = request.json
        available = data.get('available', True)  # Valoare implicită True dacă nu e specificată
        
        cursor.execute("UPDATE menu_items SET name=%s, description=%s, price=%s, available=%s, image_url=%s WHERE id=%s",
                    (data['name'], data['description'], data['price'], available, data['image_url'], data['id']))
        conn.commit()
        
        if cursor.rowcount > 0:
            return jsonify({"message": "Item updated successfully", "id": data['id']}), 200
        else:
            return jsonify({"message": "Item not found or no changes made"}), 404

    if request.method == 'DELETE':  # Ștergere produs
        data = request.json
        cursor.execute("DELETE FROM menu_items WHERE id=%s", (data['id'],))
        conn.commit()
        
        if cursor.rowcount > 0:
            return jsonify({"message": "Item deleted successfully", "id": data['id']}), 200
        else:
            return jsonify({"message": "Item not found"}), 404

    # GET → Afișează pagina și produsele
    cursor.execute("SELECT * FROM menu_items")
    products = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', products=products)