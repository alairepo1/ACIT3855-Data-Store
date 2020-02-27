import mysql.connector

db_conn = mysql.connector.connect(
    host="127.0.0.1", user="root", password="P@ssw0rd", database="ACIT3855")
db_cursor = db_conn.cursor()

db_cursor.execute('''
            CREATE TABLE order_form
            (
            id INT NOT NULL AUTO_INCREMENT,
            customer_address VARCHAR(250) NOT NULL,
            customer_id VARCHAR(250) NOT NULL,
            customer_name VARCHAR(50) NOT NULL,
            price_id INTEGER NOT NULL,
            shoe_id VARCHAR(250) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT order_form_pk PRIMARY KEY (id))
            ''')

db_cursor.execute('''
            CREATE TABLE repair_form
            (
            id INT NOT NULL AUTO_INCREMENT,
            customer_address VARCHAR(250) NOT NULL,
            customer_id VARCHAR(250) NOT NULL,
            customer_name VARCHAR(50) NOT NULL,
            damage_description VARCHAR(500) NOT NULL,
            shoe_type VARCHAR(50) NOT NULL,
            timestamp VARCHAR(250) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT repair_form_pk PRIMARY KEY (id)
            )
            ''')

db_conn.commit()
db_conn.close()
