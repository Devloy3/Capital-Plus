import sqlite3

conn = sqlite3.connect('../db/financial.db')  
cursor = conn.cursor()

sql = """
            CREATE TABLE users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Username CHAR(10),
               Password TEXT
            );
            
            CREATE TABLE inversiones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                siglas VARCHAR(10),
                cantidad DECIMAL(5,2),
                precio_compra DECIMAL(5,2),
                precio_venta DECIMAL(5,2),
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER,
                Descripcion TEXT,
                cantidad_total DECIMAL(10,2),
                interes DECIMAL(4,2) DEFAULT 0.00,
                cantidad_pagada DECIMAL(10,2) DEFAULT 0.00,
                FOREIGN KEY (user) REFERENCES users(id)
            );

            CREATE TABLE Monedas(
                Tipo CHAR(10),
                Cantidad INTEGER,
                User_id INTEGER,
                FOREIGN KEY (User_id) REFERENCES users(id)
            );
"""

cursor.executescript(sql)