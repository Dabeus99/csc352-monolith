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


# Courses CRUD
@app.route('/courses', methods=['GET'])
def get_courses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(courses)

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, credits) VALUES (%s, %s)",
        (data['title'], data['credits'])
    )
    conn.commit()
    course_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"course_id": course_id}), 201

@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE courses SET title=%s, credits=%s WHERE course_id=%s",
        (data['title'], data['credits'], course_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Course {course_id} updated."})

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM courses WHERE course_id=%s",
        (course_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Course {course_id} deleted."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
