from flask import Flask, render_template
from database import get_connection

app = Flask(__name__, template_folder="Frontend")
@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    rezultate = cursor.fetchall()
    conn.close()

    return render_template("index.html", date=rezultate)

@app.route("/sign-up")
def sign_up():
    return render_template('auth.html')

@app.route("/login")
def sign_up():
    return render_template('auth.html')




if __name__ == "__main__":
    app.run(debug = True)


