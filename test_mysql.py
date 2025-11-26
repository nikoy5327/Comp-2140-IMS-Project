import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="ims_user",
    password="yourpassword",
    database="carols_ims"
)

print("Connected!")
conn.close()
