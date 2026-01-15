from DAOfinancial import DAOfinancial
from getpass import getpass
from calculadoras_finanzas import Finanzas
from colorama import Fore,Back,Style,init
from tabulate import tabulate
import plotext as plt
from datetime import datetime

dao = DAOfinancial()
init(autoreset=True)

def titulo():
    texto = r"""
  ____            _ _        _   ____  _           
 / ___|__ _ _ __ (_) |_ __ _| | |  _ \| |_   _ ___ 
| |   / _` | '_ \| | __/ _` | | | |_) | | | | / __|
| |__| (_| | |_) | | || (_| | | |  __/| | |_| \__ \
 \____\__,_| .__/|_|\__\__,_|_| |_|   |_|\__,_|___/
           |_|                                     
 """
    print(Fore.GREEN + texto)

def menu():
    while True:
        titulo()
        print(Style.BRIGHT + "\n1. Iniciar Sesion")
        print(Style.BRIGHT + "2. Registrarse")
        print(Style.BRIGHT + "3. Salir \n")

        opcion = int(input("Opcion:"))

        if opcion == 1:
            usuario = input("Usuario: ")
            contrasenya = getpass("Contrasenya:")
            usuario_id = dao.iniciar_sesion(usuario, contrasenya)

            if usuario_id:
                interfaz(usuario_id)
        elif opcion == 2:
            r_usuario = input("Registrar Usuario: ")
            r_contrasenya = getpass("Registrar Contrasenya: ")
            resultado = dao.registrarse(r_usuario, r_contrasenya)
            print(Fore.GREEN + resultado)
        elif opcion == 3:
            break

def interfaz(id):
    while True:
        titulo()
        print(Style.BRIGHT + "\n1.Ahorro")
        print(Style.BRIGHT + "2.Inversiones")
        print(Style.BRIGHT + "3.Hacienda")
        print(Style.BRIGHT + "4.Deudas")
        print(Style.BRIGHT + "5.Calculadoras")
        print(Style.BRIGHT + "6.Cerrar Sesion \n")

        option = int(input("Escoge una opcion:"))

        if option == 1:
            ahorro = Menus(id)
            ahorro.menu_ahorro()
        elif option == 2:
            inversiones = Menus(id)
            inversiones.menu_inversion()
        elif option == 4:
            calculo = Menus(id)
            calculo.menu_deudas()
        elif option == 5:
            calculo = Menus(id)
            calculo.menu_calculadoras()
        elif option == 6:
            break

class Menus:
    def __init__(self,user):
        self.user = user
        self.calculadora = Finanzas()
    
    def menu_ahorro(self):
        while True:
            resultado = dao.consultar_saldo_total(self.user)
            print(f"\nCantidad ahorrada total: {resultado}€")
            print(Style.BRIGHT +"\n1.Registrar Saldo")
            print(Style.BRIGHT +"3.Repartir saldo/mes")
            print(Style.BRIGHT +"4.Evolucion del Ahorro")
            print(Style.BRIGHT +"5.Volver \n")

            option = int(input("Escoge:"))

            if option == 1:
                monto = float(input("Cantidad:"))
                dao.registrar_ahorro(monto,self.user)
            elif option == 3:
                años = int(input("Meses:"))
                cantidad = dao.tiempo_dinero_ahorrado(self.user,años)
                print(f"\nSaldo que se puede gastar cada mes durante {float(años/12):.2f} años es: {int(cantidad)}€")
            elif option == 4:
                grafico = dao.grafico_de_ahorro(self.user)
                cantidades = [fila[0] for fila in grafico]
                fechas = [fila[1] for fila in grafico]
                fechas_str = [datetime.strptime(f, "%Y/%m/%d") for f in fechas]
                plt.plotsize(20,30)
                plt.plot(list(range(len(fechas_str))),cantidades)
                plt.xticks(list(range(len(fechas_str))), fechas_str)
                plt.xlim(0,len(fechas))
                plt.ylim(0,max(cantidades))
                plt.show()
            elif option == 5:
                break

    def menu_calculadoras(self):
        while True:
            print(Style.BRIGHT +"\n1.Calculadora de Monto i Inflacion")
            print(Style.BRIGHT +"2.Calculadora de Desglose de Dinero")
            print(Style.BRIGHT +"3.Gastos vs Ingresos")
            print(Style.BRIGHT +"4.Volver \n")

            option = int(input("Escoge:"))

            if option == 1:
                monto = int(input("Dinero que se quiere ahorrar:"))
                años = int(input("En cuantos años se quiere conseguir:"))
                inflacion = int(input("Inflacion esperada: "))
                real,cuantia,años_2 = self.calculadora.desglose_de_ahorro(monto,años,inflacion)
                restante = real - float(cuantia)
                print(f"\n{'Dinero real ahorrado:':35}{int(real)}€")
                print(f"{'Dinero Nominal:':35}{cuantia}€")
                print(f"{'Años:':35}{años_2}")
                print(f"{'Dinero perdido por la inflacion:':35}{int(restante)}€")
            elif option == 2:
                salario = int(input("Salario Actual:"))
                desglose = self.calculadora.administracion_de_dinero(salario)
                print(desglose)
            elif option == 3:
                ingresos = int(input("Ingresos:"))
                gastos = int(input("Gastos:"))
                resultado = self.calculadora.desglose_gastos(ingresos,gastos)
                print(resultado)
            elif option == 4:
                break

    def menu_deudas(self):
        while True:
            cantidad = dao.finish_deudas(self.user)
            saldo = dao.consultar_saldo_total(self.user)
            if cantidad != None:
                print(f"\nTus deudas: {cantidad[0]}€")
            else:
                print("\nNo hay deudas")
            
            if cantidad is None or saldo is None:
                print("No hay ningun ahorro registrado\n")
            else:
                print(f"Liquidando tus deudas con el ahorro, te quedas a: {saldo[0] - cantidad[0]:.2f}€ \n")
            
            print(Style.BRIGHT +"1.Metodo bola de nieve")
            print(Style.BRIGHT +"2.Metodo Avalancha")
            print(Style.BRIGHT +"3.Insertar Deuda")
            print(Style.BRIGHT +"4.Actualizar Cantidad Pagada")
            print(Style.BRIGHT +"5.Salir \n")

            option = int(input("Escoge:"))
            
            if option== 1:
                resultado = dao.metodo_bola_de_nieve(self.user)
                headers = ["ID","DESCRIPCION","CANTIDAD TOTAL","CANTIDAD PAGADA","INTERESES"]
                print("\n"+tabulate(resultado, headers=headers, tablefmt="github"))
            elif option == 2:
                resultado = dao.metodo_avalancha(self.user)
                headers = ["ID","DESCRIPCION","CANTIDAD TOTAL","CANTIDAD PAGADA","INTERESES"]
                print("\n"+tabulate(resultado, headers=headers, tablefmt="github"))
            elif option == 3:
                descripcion = input("Descripcion:")
                cantidad_total = float(input("Cantidad Total:"))
                interes = float(input("Interes(sino 0.00):"))
                cantidad_pagada = float(input("Cantidad Pagada(sino 0.00):"))
                resp = dao.create_deuda(self.user, descripcion, cantidad_total, interes, cantidad_pagada)
                print(resp)
            elif option == 4: 
                id = int(input("Id deuda:"))
                Cantidad = int(input("Introduce la cantidad pagada:"))
                Verificador = dao.insertar_cantidad_pagada(Cantidad,id)
                print(Verificador)
            elif option == 5:
                break

    def menu_inversion(self):
        while True:
            Acciones, GananciaTotal, Patrimonio = dao.ver_el_precio_actual(self.user)
            EN = ["SIGLAS", "PRECIO ACTUAL", "PRECIO DE COMPRA", "GANANCIA"]
            print("\n"+tabulate(Acciones, headers=EN, tablefmt="github"))
            print(f"\nGanancia Total: {GananciaTotal:.2f}€")
            print(F"Patrimonio Total Actual: {Patrimonio:.2f}€")
            print(Style.BRIGHT +"\n1.Insertar Inversion")
            print(Style.BRIGHT +"2.Que inversiones tengo?")
            print(Style.BRIGHT +"3.Vender Accion")
            print(Style.BRIGHT +"4.Salir\n")
                
            option = int(input("Escoge:"))
                
            if option== 1:
                siglas = input("Siglas:")
                precio_compra = float(input("Precio_de_Compra(sino 0.00):"))
                cantidad = float(input("Cantidad(sino 0.00):"))
                res = dao.create_inversion(siglas,cantidad,precio_compra,self.user)
                print(res)
            elif option == 2:
                resultado = dao.read_inversiones(self.user)
                headers = ["ID","SIGLAS","CANTIDAD","PRECIO","PRECIO VENTA","VENTA"]
                print("\n"+tabulate(resultado, headers=headers, tablefmt="github"))
            elif option == 3:
                id = int(input("ID de la inversion:"))
                PrecioVenta = float(input("Precio de venta (0.00):"))
                Retorno = dao.sell_invesment(PrecioVenta,id)
                print(Retorno)
            elif option == 4:
                break
            

            


            

menu()