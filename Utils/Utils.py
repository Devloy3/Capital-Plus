import sqlite3

conn = sqlite3.connect('financial.db')  
cursor = conn.cursor()

sql = """
            CREATE TABLE users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Username CHAR(10),
               Password TEXT
            );
            
            CREATE TABLE inversiones(
                fecha_compra DATE,
                siglas VARCHAR(10),
                cantidad DECIMAL(5,2),
                precio_compra DECIMAL(5,2),
                user INTEGER,
                FOREIGN KEY (user) REFERENCES users(id)
            );

            CREATE TABLE ahorro(
                fecha DATE,
                cantidad DECIMAL(10,2),
                user INTEGER,
                FOREIGN KEY (user) REFERENCES users(id)
            );
                   
            CREATE TABLE deudas(
                user INTEGER,
                Descripcion TEXT,
                cantidad_total DECIMAL(10,2),
                interes DECIMAL(4,2) DEFAULT 0.00,
                cantidad_pagada DECIMAL(10,2) DEFAULT 0.00,
                plazo INTEGER,
                estado VARCHAR(20) DEFAULT 'pendiente',
                FOREIGN KEY (user) REFERENCES users(id)
            );
"""

cursor.executescript(sql)