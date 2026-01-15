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

    # ------------------------------------
    # -------USER(Register,Login)--------
    # ------------------------------------

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
    
    # --------------------------------------------
    # -------Saving(Create,Read,Saving/Time)-------
    # --------------------------------------------

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
        try:
            self.cursor.execute("SELECT cantidad FROM ahorro WHERE user=? ORDER BY fecha DESC, cantidad DESC LIMIT 1", (id,))
            cantidad = self.cursor.fetchone()
            return cantidad[0]
        except:
            return None
    
    def tiempo_dinero_ahorrado(self,id,meses):
        self.cursor.execute("SELECT cantidad FROM ahorro WHERE user=? ORDER BY fecha DESC LIMIT 1", (id,))
        cantidad_2 = self.cursor.fetchone()
        dinero_mes = cantidad_2[0] / meses

        return float(dinero_mes)
    
    def grafico_de_ahorro(self,id):
        self.cursor.execute("SELECT cantidad,fecha FROM ahorro WHERE user=? ORDER BY fecha DESC", (id,))
        fecha_cantidad = self.cursor.fetchall()
        return fecha_cantidad
    
    # ---------------------------------------------------------------
    # -------Debt(Create,Read,CreateMoneyDebt,MoneyReturned)---------
    # ---------------------------------------------------------------

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
        try: 
            self.cursor.execute("""SELECT SUM(CASE 
            WHEN interes != 0 THEN (cantidad_total * interes) - cantidad_pagada 
            ELSE cantidad_total - cantidad_pagada 
            END) AS Total FROM deudas WHERE user=?""",(id,))
            return self.cursor.fetchone()
        except:
            return None
    
    def insertar_cantidad_pagada(self,cantidad,id):
        try:
            self.cursor.execute("UPDATE deudas SET cantidad_pagada=? WHERE id=?",(cantidad,id))
            self.conn.commit()
            texto = "Se actualizo la cantidad pagada"
            return texto
        except sqlite3.Error as e:
            texto_2 = f"El error fue:{e}"
            return texto_2
    
    # ------------------------------------------------------------
    # ---------Investment(Create,Read,Current_Price,Sell_Stock)----
    # -------------------------------------------------------------

    def create_inversion(self, siglas, cantidad, precio_compra, id):
        try:
            self.cursor.execute("INSERT INTO inversiones(siglas, cantidad, precio_compra, user) VALUES (?, ?, ?, ?)", (siglas, cantidad, precio_compra, id))
            self.conn.commit()
            texto = "Inversion Insertada"
            return texto
        except sqlite3.Error as e:
            texto = f"el error ha sido: {e}"

    def read_inversiones(self,id):
        self.cursor.execute("SELECT id,siglas,cantidad,(cantidad*precio_compra) AS Precio, (cantidad*precio_venta) AS Precio_Venta, (cantidad*precio_venta-cantidad*precio_compra) AS Ganancia FROM inversiones WHERE user=?", (id,))
        Inversiones = self.cursor.fetchall()
        Inversiones2 = []

        for i,siglas,cantidad,precio,precioventa,ganancia in Inversiones:
            Inversiones2.append((i,siglas,cantidad,round(precio,2), round(precioventa,2),round(ganancia,2)))

        return Inversiones2 



    def sell_invesment(self,PrecioVenta,idInversion):
        try:
            self.cursor.execute('UPDATE inversiones SET precio_venta=? WHERE id=?',(PrecioVenta,idInversion))
            self.conn.commit()
            texto = "Venta Insertada"
            return texto
        except sqlite3.Error as e:
            texto = f"el error ha sido: {e}"

    def ver_el_precio_actual(self,id):
        self.cursor.execute("SELECT siglas,cantidad,(cantidad*precio_compra) AS Precio FROM inversiones WHERE user=? AND (precio_venta=0 OR precio_venta IS NULL)",(id,))
        resultado = self.cursor.fetchall()
        ListaTodo = []

        for siglas,cantidad,Precio in resultado:
            Accion = yf.Ticker(siglas)
            DtAccion = Accion.history(period="1mo", interval="1d")
            PrecioAccion = DtAccion["Close"].iloc[-1]
            PrecioActual = PrecioAccion*cantidad
            Conversion = float(PrecioActual)
            Ganancia =  Conversion - Precio
            ListaTodo.append((siglas,round(Conversion,2), round(Precio,2), round(Ganancia,2)))

        self.cursor.execute("SELECT cantidad FROM ahorro WHERE user=? ORDER BY fecha DESC, cantidad DESC LIMIT 1", (id,))
        Ahorro = self.cursor.fetchone()
        Ahorro = Ahorro[0] if Ahorro else 0

        GananciaSuma = sum(ganancia for siglas,conversion,precio,ganancia in ListaTodo)
        Patrimonio = sum(conversion for siglas,conversion,precio,ganancia in ListaTodo) + Ahorro

        return ListaTodo, GananciaSuma, Patrimonio