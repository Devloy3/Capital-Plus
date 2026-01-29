from DAOfinancial import DAOfinancial
from getpass import getpass
from calculadoras_finanzas import Finanzas
from colorama import Fore,Back,Style,init
from tabulate import tabulate
from datetime import datetime

Dao = DAOfinancial()
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
            usuario_id = Dao.iniciar_sesion(usuario, contrasenya)

            if usuario_id:
                interfaz(usuario_id)
        elif opcion == 2:
            r_usuario = input("Registrar Usuario: ")
            r_contrasenya = getpass("Registrar Contrasenya: ")
            resultado = Dao.registrarse(r_usuario, r_contrasenya)
            print(Fore.GREEN + resultado)
        elif opcion == 3:
            break

def interfaz(id):
    while True:
        titulo()
        print(Fore.GREEN + Style.BRIGHT + "\nBienvenidos a Capital plus!! Que quieres hacer?")
        print(Style.BRIGHT + "\n1.Ahorro")
        print(Style.BRIGHT + "2.Inversiones")
        print(Style.BRIGHT + "3.Deudas")
        print(Style.BRIGHT + "4.Calculadoras")
        print(Style.BRIGHT + "5.Cerrar Sesion \n")

        option = int(input("Escoge una opcion:"))

        if option == 1:
            ahorro = Menus(id)
            ahorro.menu_ahorro()
        elif option == 2:
            inversiones = Menus(id)
            inversiones.menu_inversion()
        elif option == 3:
            calculo = Menus(id)
            calculo.menu_deudas()
        elif option == 4:
            calculo = Menus(id)
            calculo.menu_calculadoras()
        elif option == 5:
            break

class Menus:
    def __init__(self,user):
        self.user = user
        self.calculadora = Finanzas()
    
    def menu_ahorro(self):
        while True:
            Patrimonio = Dao.PrecioActual(self.user)
            Resultado = Dao.SaldoTotal(self.user)
            
            if Patrimonio[2] == 0 and Resultado == 0: 
                 print(Fore.RED + Style.BRIGHT + "\nNo hay datos")
            elif Patrimonio[2] != Resultado:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\nPatrimonio Total: {Patrimonio[2]:.2f}€")
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"Cantidad de Liquidez: {Resultado}€")
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\nCantidad ahorrada total: {Resultado}€")

            print(Style.BRIGHT +"\n1.Registrar Saldo")
            print(Style.BRIGHT +"2.Repartir saldo/mes")
            print(Style.BRIGHT +"3.Evolucion del Ahorro")
            print(Style.BRIGHT +"4.Volver \n")

            option = int(input("Escoge:"))

            if option == 1:
                Monto = float(input("Cantidad(sino 0.00):"))
                Res = Dao.RegistroAhorro(Monto,self.user)
                print(Res)
            elif option == 2:
                Años = int(input("Meses:"))
                Cantidad = Dao.TiempoDinero(self.user,Años)
                print(f"\nSaldo que se puede gastar cada mes durante {float(Años/12):.2f} años es de: {int(Cantidad)}€")
            elif option == 3:
                Evolucion = Dao.EvolucionAhorro(self.user)
                
                if not Evolucion:
                   pass
                else: 
                    headers = ["CANTIDAD","FECHA"]
                    print("\n"+tabulate(Evolucion, headers=headers, tablefmt="github"))
            
            elif option == 4:
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
            Cantidad = Dao.FinishDeudas(self.user)
            Ahorro = Dao.SaldoTotal(self.user)
            
            if Cantidad != 0 and Ahorro != 0:
                Resto = Ahorro - Cantidad

                print(Style.BRIGHT + f"\nSuma de Deudas:\033[31m{Cantidad}€\033[0m")
                
                if Resto < 0:
                    print(Fore.RED + Style.BRIGHT +"No puedes restar deuda con tus Ahorros\n")
                else:
                    print(f"Deudas - Ahorro:{float(Resto):.2f}€\n")
            
            elif Cantidad != 0:
                print(f"\nSuma de Deudas:\033[31m{Cantidad}€\033[0m\n")
            else:
                print(Fore.GREEN + Style.BRIGHT + "\nNo tienes deudas\n")
            
            print(Style.BRIGHT +"1.Metodo bola de nieve")
            print(Style.BRIGHT +"2.Metodo Avalancha")
            print(Style.BRIGHT +"3.Insertar Deuda")
            print(Style.BRIGHT +"4.Actualizar Cantidad Pagada")
            print(Style.BRIGHT +"5.Salir \n")

            option = int(input("Escoge:"))
            
            if option== 1:
                Resultado = Dao.BolaNieve(self.user)
                
                if not Resultado:
                    pass
                else:
                    headers = ["ID","DESCRIPCION","CANTIDAD TOTAL","CANTIDAD PAGADA","INTERESES"]
                    print("\n"+tabulate(Resultado, headers=headers, tablefmt="github"))
            
            elif option == 2:
                Resultado = Dao.Avalancha(self.user)
                
                if not Resultado:
                   pass
                else:
                    headers = ["ID","DESCRIPCION","CANTIDAD TOTAL","CANTIDAD PAGADA","INTERESES"]
                    print("\n"+tabulate(Resultado, headers=headers, tablefmt="github"))
            
            elif option == 3:
                Descripcion = input("Descripcion:")
                CantidadTotal = float(input("Cantidad Total:"))
                Interes = float(input("Interes(sino 0.00):"))
                Resp = Dao.CreateDeuda(self.user, Descripcion, CantidadTotal, Interes)
                print(Resp)
            elif option == 4: 
                Id = int(input("Id deuda:"))
                Cantidad = float(input("Introduce la cantidad pagada(sino 0.00):"))
                Resp = Dao.CantidadPagada(Cantidad,Id)
                print(Resp)
            elif option == 5:
                break

    def menu_inversion(self):
        while True:
            Acciones, GananciaTotal, _ , ValorAccion = Dao.PrecioActual(self.user)
            
            if ValorAccion == 0 and GananciaTotal == 0:
                print(Fore.RED + Style.BRIGHT + "\nNo hay datos")
            else:
                EN = ["SIGLAS", "PRECIO ACTUAL", "PRECIO DE COMPRA", "GANANCIA"]
                print("\n"+tabulate(Acciones, headers=EN, tablefmt="github"))
                print(f"\nGanancia Total: {GananciaTotal:.2f}€")
                print(f"Valor del Portafolio: {ValorAccion:.2f}€")
            
            print(Style.BRIGHT +"\n1.Insertar Inversion")
            print(Style.BRIGHT +"2.Insertar Moneda")
            print(Style.BRIGHT +"3.Consultar Inversiones")
            print(Style.BRIGHT +"4.Consultar Criptomonedas o Monedas")
            print(Style.BRIGHT +"5.Venta de Accion")
            print(Style.BRIGHT +"6.Salir\n")
                
            option = int(input("Escoge:"))
                
            if option== 1:
                print("\nTiene que ser las siglas de yahoo finance!!!\n")
                Siglas = input("Siglas:")
                PrecioCompra = float(input("Precio_de_Compra(sino 0.00):"))
                Cantidad = float(input("Cantidad(sino 0.00):"))
                Resp = Dao.CreateInversion(Siglas,Cantidad,PrecioCompra,self.user)
                print(Resp)
            elif option == 3:
                Resultado = Dao.ReadInversiones(self.user)

                if not Resultado:
                    pass
                else:
                    headers = ["ID","SIGLAS","CANTIDAD","PRECIO","PRECIO VENTA","VENTA"]
                    print("\n"+tabulate(Resultado, headers=headers, tablefmt="github"))
            
            elif option == 5:
                Id = int(input("ID de la inversion:"))
                PrecioVenta = float(input("Precio de venta sino(0.00):"))
                Resp = Dao.SellInvesment(PrecioVenta,Id)
                print(Resp)
            elif option == 4:
                Monedas = Dao.ConsultaMonedas(self.user)
                
                if not Monedas:
                    pass
                else:
                    headers = ["SIGLAS","CANTIDAD","EUROS"]
                    print("\n"+tabulate(Monedas, headers=headers, tablefmt="github"))
            
            elif option == 2:
                print("\nTiene que ser las siglas de yahoo finance!!!\n")
                Siglas = input("Siglas:")
                Cantidad = float(input("Cantidad(sino 0.00):"))
                Resp = Dao.CreateMoney(Siglas,Cantidad,self.user)
                print(Resp)
            elif option == 6:
                break
                
            

            


            

menu()