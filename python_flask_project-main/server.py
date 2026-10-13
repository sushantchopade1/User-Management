from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
import sqlite3


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'upload')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT,
            hobby TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# create routes
@app.route("/")  # decorator
@app.route("/home")  # decorator
def home():
    return render_template('home.html')


@app.route('/market')
def market():
    items = [
        {'id': 1, 'name': 'phone', 'barcode': '232as', 'price': 200},
        {'id': 2, 'name': 'laptop', 'barcode': '12ds', 'price': 120},
        {'id': 3, 'name': 'keyboard', 'barcode': '4ds', 'price': 100},
    ]
    return render_template('market.html', items=items)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        city = request.form.get('city')
        hobby = request.form.get('hobby')

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users(user_name, email, city, hobby) VALUES(?, ?, ?, ?)",
            (user_name, email, city, hobby)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('get_users'))
    return render_template('add_user.html')


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        user_file = request.files['user_file']
        if user_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_file.filename))
            user_file.save(file_path)
            return render_template('success.html', operation='File Uploading', method='upload_file')
        return 'File Uploading Failed!'
    return render_template('upload_file.html')


@app.route('/user_profile/<int:id>', methods=['GET'])
def user_profile(id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("user_profile.html", user=user)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return render_template('success.html', operation="User Deleted", method='get_users')


@app.route('/update_user/<int:id>', methods=['POST', 'GET'])
def update_user(id):
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        city = request.form.get('city')
        hobby = request.form.get('hobby')

        conn = get_db_connection()
        conn.execute(
            """
            UPDATE users
            SET user_name = ?, email = ?, city = ?, hobby = ?
            WHERE id = ?
            """,
            (user_name, email, city, hobby, id)
        )
        conn.commit()
        conn.close()
        return render_template('success.html', operation='User Updated', method='user_profile', id=id)

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("update_user.html", user=user)


@app.route('/users')
def get_users():
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(id) FROM users").fetchone()[0]
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('users.html', users=rows, count=count)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)