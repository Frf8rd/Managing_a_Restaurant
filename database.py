import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.127.126.26",  # Sau "127.127.126.50"
            port=3306,
            user="root",
            password="",  # Parola ta
            database="restaurant_db"
        )

        if conn.is_connected():
            print("Conectare reușită la MySQL!")
        
        return conn  # Returnăm conexiunea pentru utilizare în altă parte

    except mysql.connector.Error as e:
        print(f"Eroare la conectare: {e}")
        return None  # În caz de eroare, returnăm None

# Testare conexiune
conn = get_connection()
if conn:
    conn.close()  # Închidem conexiunea după verificare
