import mysql.connector

db_conn = mysql.connector.connect(host="127.0.0.1",user="root",password="P@ssw0rd",database="ACIT3855")

db_cursor = db_conn.cursor()

db_cursor.execute('''
    DROP TABLE order_form, repair_form
''')

db_conn.commit()
db_conn.close()