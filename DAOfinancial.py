from datetime import date
import sqlite3
import bcrypt
from colorama import Fore,Back,Style,init

init(autoreset=True)

class DAOfinancial:
    def __init__(self):
        self.conn = sqlite3.connect('./db/financial.db')  # Crea el archivo si no existe
        self.cursor = self.conn.cursor()

    def registrarse(self,user,contrasenya):
        password = contrasenya.encode("utf-8")
        salt = bcrypt.gensalt()
        password_encriptada = bcrypt.hashpw(password, salt)

        try:
            self.cursor.execute("INSERT INTO users(Username,Password) VALUES (?,?)", (user,password_encriptada))
            self.conn.commit()
            texto = "\nRegistro hecho!" 
            return texto
        except:
            print("Ha fallado la conexion con la base de datos")

    def iniciar_sesion(self,user,contrasenya):
    
        self.cursor.execute("SELECT * FROM users WHERE Username=?",(user,))
        usuario = self.cursor.fetchone()
        
        if usuario:
            password = usuario[2]
            id = usuario[0]
            password_byte = contrasenya.encode("utf-8")
            
            if bcrypt.checkpw(password_byte, password):
                return id
            else:
                print(Fore.RED +"\nContrasenya Incorrecta")
        else:
            print(Fore.RED + "\nUsuario Incorrecto")

    def registrar_ahorro(self,dinero,id):
        fecha = date.today()
        fecha_string = fecha.strftime("%Y/%m/%d")
        try:
            self.cursor.execute("INSERT INTO ahorro(fecha,cantidad,user) VALUES (?,?,?)", (fecha_string,dinero,id))
            self.conn.commit()
            print("Se ha insertado perfectamente")
        except sqlite3.Error as e:
            print(f"No se ha insertado correctamente:{e}")

    def consultar_saldo_total(self,id):
        self.cursor.execute("SELECT cantidad FROM ahorro WHERE user=? ORDER BY fecha DESC, cantidad DESC LIMIT 1", (id,))
        cantidad = self.cursor.fetchone()
        return cantidad
    
    def tiempo_dinero_ahorrado(self,id,meses):
        self.cursor.execute("SELECT cantidad FROM ahorro WHERE user=? ORDER BY fecha DESC LIMIT 1", (id,))
        cantidad_2 = self.cursor.fetchone()
        dinero_mes = cantidad_2[0] / meses

        return float(dinero_mes)
    
    def create_deuda(self, id, descripcion, cantidad_total, interes, cantidad_pagada):
        try:
            self.cursor.execute("INSERT INTO deudas(user, descripcion, cantidad_total, interes, cantidad_pagada) VALUES (?, ?, ?, ?, ?)", (id, descripcion, cantidad_total, interes, cantidad_pagada))
            self.conn.commit()
            intento = "Se inserto correctamente"
            return intento
        except sqlite3.Error as e:
            texto = f"El Error ha sido:{e}"
            return texto
    
    def metodo_bola_de_nieve(self,id):
        self.cursor.execute("SELECT Descripcion,cantidad_total,cantidad_pagada,estado FROM deudas WHERE user=? ORDER BY cantidad_total ASC",(id,))
        return self.cursor.fetchall()
    
    def metodo_avalancha(self,id):
        self.cursor.execute("SELECT Descripcion,cantidad_total,cantidad_pagada,interes,estado FROM deudas WHERE user=? ORDER BY interes ASC",(id,))
        return self.cursor.fetchall()

    def finish_deudas(self,id):
        self.cursor.execute("SELECT (SUM(cantidad_total) - SUM(cantidad_pagada)) AS Total FROM deudas WHERE user=?",(id,))
        return self.cursor.fetchone()
    
    def insertar_cantidad_pagada(self,cantidad,descripcion):
        try:
            self.cursor.execute("UPDATE deudas SET cantidad_pagada=? WHERE Descripcion=?",(cantidad,descripcion))
            self.conn.commit()
            texto = f" Se actualizo {descripcion}"
            return texto
        except sqlite3.Error as e:
            texto_2 = f"El error fue:{e}"
            return texto_2