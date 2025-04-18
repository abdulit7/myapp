import mysql.connector

try:
    connection = mysql.connector.connect(
        host="200.200.200.23",
        user="root",
        password="Pak@123",
        database="itasset",
        auth_plugin='mysql_native_password'
    )
    print("Database connection successful")

    cursor = connection.cursor()

    # Define the columns and their data types
    columns_to_check = {
        "name": "VARCHAR(255)",
        "category": "VARCHAR(255)",
        "company": "VARCHAR(255)",
        "model": "VARCHAR(255)",
        "serial_no": "VARCHAR(255)",
        "purchaser": "VARCHAR(255)",
        "purchase_date": "DATE",
        "location": "VARCHAR(255)",
        "warranty": "VARCHAR(255)",
        "price": "DECIMAL(10,2)",
        "status": "VARCHAR(255)",
        "bill_copy": "VARCHAR(255)",
        "image_path": "VARCHAR(255)"
    }

    # Check and add each column
    for column_name, column_type in columns_to_check.items():
        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'itasset'
            AND TABLE_NAME = 'component'
            AND COLUMN_NAME = %s
        """, (column_name,))
        column_exists = cursor.fetchone()[0] > 0

        if not column_exists:
            # Add the column if it doesn't exist
            cursor.execute(f"ALTER TABLE component ADD COLUMN {column_name} {column_type}")
            connection.commit()
            print(f"Column '{column_name}' added successfully with type {column_type}")
        else:
            print(f"Column '{column_name}' already exists, skipping")

    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Database connection closed")