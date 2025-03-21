from flask import Flask, render_template
from database import get_connection

app = Flask(__name__, template_folder="Frontend")
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    rezultate = cursor.fetchall()
    conn.close()

    return render_template("index.html", date=rezultate)





if __name__ == "__main__":
    app.run(debug = True)


