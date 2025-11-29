import pandas as pd
import requests 
import plotext as pl

def grafica_inflacion():
    response = requests.get("https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24077")
    data = response.json()
   
    # Creamos el dataframe
    df = pd.DataFrame(data)
    # Normalizamos el json dentro del dataframe
    df_exp = pd.json_normalize(df['Data'][0])
    # Eliminamos columnas innecessarias
    df_exp.drop(columns=["Secreto", "FK_TipoDato","Fecha"], inplace=True)
    # Creamos una columna nueva que se guardara como string el año y el mes
    df_exp['Periodo'] = df_exp['Anyo'].astype(str) + "-" + df_exp['FK_Periodo'].astype(str).str.zfill(2)
    # Ordenamos por año y mes
    df_exp = df_exp.sort_values(['Anyo','FK_Periodo'])
    # Calculamos en una nueva columna la inflacio interanual
    df_exp['Inflacion_interanual'] = df_exp['Valor'].pct_change(12) * 100
    # Creamos un nuevo dataframe con los datos que nos interesan
    df_nuevo = pd.DataFrame(df_exp[['Periodo','Inflacion_interanual']])
    # Por ultimo hacemos que solo sean dos decimales y ordenamos el indice
    df_nuevo["Inflacion_interanual"] = df_nuevo["Inflacion_interanual"].round(2)
    df_nuevo.sort_index(inplace=True)

    inflacion = df_nuevo.head(n=13)

    promedio = inflacion["Inflacion_interanual"].mean()

    x = inflacion["Periodo"].tolist()
    y = inflacion["Inflacion_interanual"].tolist()

    pl.plot(range(len(x)),y)
    pl.title("Gráfico de Inflacion Anual")
    pl.ylabel("Inflacion")
    pl.xlabel("Mes-Año")
    pl.show()