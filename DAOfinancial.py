from datetime import date
import sqlite3
import bcrypt
from colorama import Fore,Back,Style,init
import yfinance as yf


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
    # ahrro registro
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
    
    def inflacion_dinero(self,id,interes):
        self.cursor.execute("SELECT cantidad,fecha FROM ahorro WHERE user=? ORDER BY fecha ", (id,))
        resultado = self.cursor.fetchall()

        

    # Crud mas o menos de deuda
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
        self.cursor.execute("SELECT id,Descripcion,cantidad_total,cantidad_pagada,interes FROM deudas WHERE user=? ORDER BY cantidad_total ASC",(id,))
        return self.cursor.fetchall()
    
    def metodo_avalancha(self,id):
        self.cursor.execute("SELECT id,Descripcion,cantidad_total,cantidad_pagada,interes FROM deudas WHERE user=? ORDER BY interes ASC",(id,))
        return self.cursor.fetchall()

    def finish_deudas(self,id):
        self.cursor.execute("""SELECT SUM(CASE 
        WHEN interes != 0 THEN (cantidad_total * interes) - cantidad_pagada 
        ELSE cantidad_total - cantidad_pagada 
        END) AS Total FROM deudas WHERE user=?""",(id,))
        return self.cursor.fetchone()
    
    def insertar_cantidad_pagada(self,cantidad,id):
        try:
            self.cursor.execute("UPDATE deudas SET cantidad_pagada=? WHERE id=?",(cantidad,id))
            self.conn.commit()
            texto = f" Se actualizo la cantidad pagada"
            return texto
        except sqlite3.Error as e:
            texto_2 = f"El error fue:{e}"
            return texto_2
    
    # Crud mas o menos de Inversion
    def create_inversion(self, siglas, cantidad, precio_compra, id):
        try:
            self.cursor.execute("INSERT INTO inversiones(siglas, cantidad, precio_compra, user) VALUES (?, ?, ?, ?)", (siglas, cantidad, precio_compra, id))
            self.conn.commit()
            texto = "Inversion Insertada"
            return texto
        except sqlite3.Error as e:
            texto = f"el error ha sido: {e}"

    def read_inversiones(self,id):
        self.cursor.execute("SELECT id,siglas,cantidad,(cantidad*precio_compra) AS Precio,(cantidad*precio_venta-precio_compra) AS Venta FROM inversiones WHERE user=?", (id,))
        return self.cursor.fetchall()
    
    def ver_el_precio_actual(self,id):
        self.cursor.execute("SELECT siglas,cantidad,(cantidad*precio_compra) AS Precio FROM inversiones WHERE user=? AND precio_venta=0",(id,))
        resultado = self.cursor.fetchall()
        lista = []

        for siglas,cantidad,Precio in resultado:
            accion = yf.Ticker(siglas)
            dt_accion = accion.history(period="1mo", interval="1d")
            precio_accion = dt_accion["Close"].iloc[-1]
            precio_actual = precio_accion*cantidad
            conversion = float(precio_actual)
            ganancia =  conversion - Precio
            lista.append((siglas,round(conversion,2), round(Precio,2), round(ganancia,2)))
        
        return lista