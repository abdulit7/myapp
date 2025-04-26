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

        # Drop tables in reverse order of dependencies
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        cur.execute("DROP TABLE IF EXISTS deployed_assets")
        cur.execute("DROP TABLE IF EXISTS deployed_components")
        cur.execute("DROP TABLE IF EXISTS deployed_consumables")
        cur.execute("DROP TABLE IF EXISTS disposed_assets")
        cur.execute("DROP TABLE IF EXISTS disposed_components")
        cur.execute("DROP TABLE IF EXISTS assets")
        cur.execute("DROP TABLE IF EXISTS components")
        cur.execute("DROP TABLE IF EXISTS consumables")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS department")
        cur.execute("DROP TABLE IF EXISTS category")
        cur.execute("DROP TABLE IF EXISTS location")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        # Create category table (removed image_path)
        cur.execute("""
            CREATE TABLE category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # Create location table
        cur.execute("""
            CREATE TABLE location (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # Create department table
        cur.execute("""
            CREATE TABLE department (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # Create users table
        cur.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                emp_id VARCHAR(50) NOT NULL,
                password VARCHAR(255),
                branch VARCHAR(100) NOT NULL,
                department_id INT,
                can_login TINYINT(1) NOT NULL DEFAULT 0,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT uk_emp_id UNIQUE (emp_id),
                FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE SET NULL
            )
        """)

        cur.execute("CREATE INDEX idx_can_login ON users(can_login)")
        cur.execute("CREATE INDEX idx_department_id ON users(department_id)")

        # Create assets table
        cur.execute("""
            CREATE TABLE assets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Available',
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL
            )
        """)

        # Create deployed_assets table
        cur.execute("""
            CREATE TABLE deployed_assets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to INT,
                user_department VARCHAR(255),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL,
                FOREIGN KEY (deployed_to) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        cur.execute("CREATE INDEX idx_deployed_to ON deployed_assets(deployed_to)")

        # Create components table
        cur.execute("""
            CREATE TABLE components (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                remaining_qty INT,
                min_qty INT,
                model_no VARCHAR(100),
                status VARCHAR(50) DEFAULT 'Available',
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL
            )
        """)

        # Create deployed_components table
        cur.execute("""
            CREATE TABLE deployed_components (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                remaining_qty INT,
                min_qty INT,
                model_no VARCHAR(100),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to INT,
                user_department VARCHAR(255),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL,
                FOREIGN KEY (deployed_to) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        cur.execute("CREATE INDEX idx_deployed_to ON deployed_components(deployed_to)")

        # Create consumables table
        cur.execute("""
            CREATE TABLE consumables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                remaining_qty INT,
                min_qty INT,
                model_no VARCHAR(100),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL
            )
        """)

        # Create deployed_consumables table
        cur.execute("""
            CREATE TABLE deployed_consumables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(255),
                model VARCHAR(255),
                serial_no VARCHAR(255),
                purchaser VARCHAR(255),
                location VARCHAR(255),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(255),
                total_qty INT NOT NULL,
                remaining_qty INT,
                min_qty INT,
                model_no VARCHAR(100),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                status VARCHAR(50) DEFAULT 'Deployed',
                deployed_to INT,
                deploy_target_type VARCHAR(50),
                deploy_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL,
                FOREIGN KEY (deployed_to) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        cur.execute("CREATE INDEX idx_deployed_to ON deployed_consumables(deployed_to)")

        # Create disposed_assets table
        cur.execute("""
            CREATE TABLE disposed_assets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                company VARCHAR(100),
                model VARCHAR(100),
                serial_no VARCHAR(100),
                purchaser VARCHAR(100),
                location VARCHAR(100),
                location_id INT,
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                warranty VARCHAR(50),
                bill_copy VARCHAR(255),
                purchase_date DATE,
                image_path VARCHAR(255),
                disposal_type ENUM('Scrap', 'Dispose', 'Sold') NOT NULL,
                disposal_date DATE NOT NULL,
                amount_earned DECIMAL(10, 2),
                disposal_reason TEXT,
                disposal_location VARCHAR(255),
                sale_details TEXT,
                sold_to VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL
            )
        """)

        # Create disposed_components table
        cur.execute("""
            CREATE TABLE disposed_components (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                category_id INT,
                company VARCHAR(100),
                model VARCHAR(100),
                serial_no VARCHAR(100),
                purchaser VARCHAR(100),
                location VARCHAR(255),
                location_id INT,
                warranty VARCHAR(50),
                price DECIMAL(10, 2),
                purchase_cost DECIMAL(10, 2),
                purchase_date DATE,
                image_path VARCHAR(255),
                model_no VARCHAR(100),
                min_qty INT,
                total_qty INT,
                remaining_qty INT,
                disposal_type ENUM('Scrap', 'Dispose', 'Sold') NOT NULL,
                disposal_date DATE NOT NULL,
                amount_earned DECIMAL(10, 2),
                disposal_reason TEXT,
                disposal_location VARCHAR(255),
                sale_details TEXT,
                sold_to VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL,
                FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE SET NULL
            )
        """)

        cur.execute("CREATE INDEX idx_disposal_type ON disposed_components(disposal_type)")
        cur.execute("CREATE INDEX idx_disposal_date ON disposed_components(disposal_date)")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cur.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    create_database()