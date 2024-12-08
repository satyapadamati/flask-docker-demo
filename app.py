from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="database-1.cxwwk8yooc3q.us-east-2.rds.amazonaws.com",  # Replace with AWS endpoint
        user="admin",                      # Replace with AWS MySQL username
        password="Admin123",                  # Replace with AWS MySQL password
        database="mydb1"                    # Replace with AWS database name
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/create', methods=['POST'])
def create_user():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
                   (data['name'], data['email'], data['age']))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s",
                   (data['name'], data['email'], data['age'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
