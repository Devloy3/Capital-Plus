import pandas as pd
import requests 
import plotext as pl

def grafica_inflacion():
    response = requests.get("https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC251856?nult=13")
    data = response.json()
   
    df = pd.DataFrame(data)
    df_nuevo = pd.json_normalize(df["Data"])

    df_nuevo.drop(columns=["Fecha", "FK_TipoDato", "Secreto"], inplace=True)

    df_nuevo ["FK_Periodo"] = df_nuevo["FK_Periodo"].astype(str)  
    df_nuevo["Anyo"] = df_nuevo["Anyo"].astype(str)

    df_nuevo["Periodo"] = df_nuevo["FK_Periodo"] + "/" + df_nuevo["Anyo"]
    
    df_nuevo.drop(columns=["FK_Periodo", "Anyo"], inplace=True)
    

    lista_periodo = df_nuevo["Periodo"].to_list()
    x = range(len(lista_periodo))
    y = df_nuevo["Valor"].to_list()

    valor_maximo = df_nuevo["Valor"].max()

    valor_minimo = df_nuevo["Valor"].min()

    pl.plot(x,y,  marker="dot", color="red")
    pl.title("Inflacion Interanual")
    pl.yscale("linear")
    pl.ylim(valor_minimo,valor_maximo)
    pl.xticks(x, lista_periodo)
    pl.canvas_color("black")
    pl.axes_color("black")
    pl.plotsize(60,35)
    pl.show()

    

    


    
