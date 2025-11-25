from DAOfinancial import DAOfinancial
from getpass import getpass
from calculadoras_finanzas import Finanzas
from colorama import Fore,Back,Style,init

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
            print(Style.BRIGHT +"\n1.Registrar Saldo")
            print(Style.BRIGHT +"2.Consultar saldo ahorrado actual")
            print(Style.BRIGHT +"3.Repartir saldo/mes por años")
            print(Style.BRIGHT +"4.Saldo perdido por inflacion")
            print(Style.BRIGHT +"5.Volver \n")

            option_2 = int(input("Escoge:"))

            if option_2 == 1:
                monto = float(input("Cantidad:"))
                dao.registrar_ahorro(monto,self.user)
            elif option_2 == 2:
                resultado = dao.consultar_saldo_total(self.user)
                print(f"\nCantidad ahorrada total: {resultado[0]}€")
            elif option_2 == 3:
                años = int(input("Meses:"))
                cantidad = dao.tiempo_dinero_ahorrado(self.user,años)
                print(f"\nSaldo que se puede gastar cada mes durante {float(años/12):.2f} años es: {int(cantidad)}€")
            elif option_2 == 5:
                break

    def menu_calculadoras(self):
        while True:
            print(Style.BRIGHT +"\n1.Calculadora de Monto i Inflacion")
            print(Style.BRIGHT +"2.Calculadora de Desglose de Dinero")
            print(Style.BRIGHT +"3.Gastos vs Ingresos")
            print(Style.BRIGHT +"4.Volver \n")

            option_3 = int(input("Escoge:"))

            if option_3 == 1:
                monto = int(input("Dinero que se quiere ahorrar:"))
                años = int(input("En cuantos años se quiere conseguir:"))
                inflacion = int(input("Inflacion esperada: "))
                real,cuantia,años_2 = self.calculadora.desglose_de_ahorro(monto,años,inflacion)
                restante = real - float(cuantia)
                print(f"\n{'Dinero real ahorrado:':35}{int(real)}€")
                print(f"{'Dinero Nominal:':35}{cuantia}€")
                print(f"{'Años:':35}{años_2}")
                print(f"{'Dinero perdido por la inflacion:':35}{int(restante)}€")
            elif option_3 == 2:
                salario = int(input("Salario Actual:"))
                desglose = self.calculadora.administracion_de_dinero(salario)
                print(desglose)
            elif option_3 == 3:
                ingresos = int(input("Ingresos:"))
                gastos = int(input("Gastos"))
                resultado = self.calculadora.desglose_gastos(ingresos,gastos)
                print(resultado)
            elif option_3 == 4:
                break

    def menu_deudas(self):
        while True:
            cantidad = dao.finish_deudas(self.user)
            print(f"Para acabar con tus deudas: {int(cantidad)}€\n")
            print("1.Metodo bola de nieve")
            print("2.Metodo")


            

menu()