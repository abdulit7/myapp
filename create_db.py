import mysql.connector

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="200.200.200.23",
            user="root",
            password="Pak@123"
        )
        cur = connection.cursor()

        # Create database if it doesn't exist
        cur.execute("CREATE DATABASE IF NOT EXISTS itasset")
        cur.execute("USE itasset")

        # Create assets table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Available',
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create deployed_assets table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS deployed_assets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to VARCHAR(255),
                user_department VARCHAR(255),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create components table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Available',
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create deployed_components table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS deployed_components (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to VARCHAR(255),
                user_department VARCHAR(255),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create consumables table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS consumables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Available',
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create deployed_consumables table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS deployed_consumables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                price DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to VARCHAR(255),
                deploy_target_type VARCHAR(50),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        print("Database and tables created successfully")

    except mysql.connector.Error as error:
        print(f"Failed to create database: {error}")
    finally:
        if connection.is_connected():
            cur.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    create_database()