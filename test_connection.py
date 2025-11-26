import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        # Try different connection methods
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Try root first
            password=input("Enter MySQL root password: "),
            database='mysql'  # Connect to default mysql database first
        )
        
        if connection.is_connected():
            print("✓ Successfully connected to MySQL!")
            
            cursor = connection.cursor()
            
            # Check if our database exists
            cursor.execute("SHOW DATABASES LIKE 'carols_ims'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print("✓ carols_ims database exists")
                cursor.execute("USE carols_ims")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"✓ Tables in carols_ims: {tables}")
            else:
                print("✗ carols_ims database doesn't exist yet")
                
    except Error as e:
        print(f"✗ Connection failed: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    test_connection()