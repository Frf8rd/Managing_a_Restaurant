from flask import Blueprint, render_template, request, jsonify
from database import get_connection
import os
from werkzeug.utils import secure_filename
import uuid

dashboard_bp = Blueprint('dashboard', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard_bp.route('/dashboard', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if request.method == 'POST':
            # Verificare fișier
            if 'image' not in request.files:
                return jsonify({"message": "No image uploaded"}), 400
                
            file = request.files['image']
            if file.filename == '':
                return jsonify({"message": "No selected image"}), 400
                
            if not (file and allowed_file(file.filename)):
                return jsonify({"message": "Invalid file type"}), 400

            # Procesare imagine
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # Obține datele din formular
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            
            # Validează datele
            if not all([name, description, price]):
                return jsonify({"message": "Missing required fields"}), 400
            
            # Adaugă în baza de date
            cursor.execute(
                "INSERT INTO menu_items (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
                (name, description, price, unique_filename)
            )
            conn.commit()
            
            return jsonify({
                "message": "Item added successfully",
                "id": cursor.lastrowid,
                "image_url": unique_filename
            }), 201

        elif request.method == 'PUT':
            # Obține datele din formular
            id = request.form.get('id')
            existing_image = request.form.get('existing_image')
            name = request.form.get('name')
            description = request.form.get('description')
            price = request.form.get('price')
            file = request.files.get('image')
            
            # Validează datele
            if not all([id, name, description, price, existing_image]):
                return jsonify({"message": "Missing required fields"}), 400
            
            image_to_save = existing_image
            
            # Procesează noua imagine dacă există
            if file and allowed_file(file.filename):
                # Șterge vechea imagine
                old_path = os.path.join(UPLOAD_FOLDER, existing_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
                
                # Salvează noua imagine
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                image_to_save = unique_filename
            
            # Actualizează în baza de date
            cursor.execute(
                "UPDATE menu_items SET name=%s, description=%s, price=%s, image_url=%s WHERE id=%s",
                (name, description, price, image_to_save, id)
            )
            conn.commit()
            
            return jsonify({
                "message": "Item updated successfully",
                "id": id,
                "image_url": image_to_save
            }), 200

        elif request.method == 'DELETE':
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({"message": "Missing product ID"}), 400
                
            # Obține imaginea asociată
            cursor.execute("SELECT image_url FROM menu_items WHERE id=%s", (data['id'],))
            item = cursor.fetchone()
            
            if item and item['image_url']:
                # Șterge imaginea
                file_path = os.path.join(UPLOAD_FOLDER, item['image_url'])
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Șterge din baza de date
            cursor.execute("DELETE FROM menu_items WHERE id=%s", (data['id'],))
            conn.commit()
            
            return jsonify({
                "message": "Item deleted successfully",
                "id": data['id']
            }), 200

        # GET - Afișează pagina și produsele
        cursor.execute("SELECT * FROM menu_items")
        products = cursor.fetchall()
        return render_template('dashboard.html', products=products)

    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Server error: {str(e)}"}), 500
        
    finally:
        conn.close()