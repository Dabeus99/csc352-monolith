from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# --- MySQL connection configuration ---
db_config = {
    'host': os.getenv("DB_URL"),
    'user': 'admin',
    'password': os.getenv("PASSWORD"),
    'database': 'school',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**db_config)

# Students CRUD
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, major, year) VALUES (%s, %s, %s)",
        (data['name'], data['major'], data['year'])
    )
    conn.commit()
    student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"student_id": student_id}), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=%s, major=%s, year=%s WHERE student_id=%s",
        (data['name'], data['major'], data['year'], student_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Student {student_id} updated."})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Student {student_id} deleted."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)