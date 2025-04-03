from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection function
def get_database_connection():
    try:
        conn = mysql.connector.connect(
            host="200.200.200.23",  # Replace with your MySQL server IP
            user="root",  # Your MySQL username
            password="Pak@123",  # Your MySQL password
            database="itasset",  # Your database name
            auth_plugin="mysql_native_password"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# API to fetch categories from the database
@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_database_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM category")
        categories = cursor.fetchall()
        conn.close()

        # Convert data to JSON format
        return jsonify([
            {"id": row[0], "name": row[1], "description": row[2]}
            for row in categories
        ])
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
