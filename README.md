
# Capital Plus

Capital Plus, es una fintech para ordenar las finanzas personales, orientada a 
Inversion, Ahorro y Deudas, donde varios usuarios pueden guardar diferente 
informacion en la app.

---

## Problema 

La mayoría de aplicaciones financieras disponibles no abordan el problema de una 
manera sencilla ni transparente.

Entre las principales dificultades encontradas:

  - No permiten visualizar de forma clara la información de inversiones o deudas.

  - Prácticamente no existen apps que permitan registrar y gestionar deudas    
    personales sin vincular cuentas bancarias.

  - Muchas aplicaciones requieren acceso a datos bancarios sensibles, sin que el 
    usuario tenga certeza de cómo se almacenan o utilizan esos datos.

Esto deja a los usuarios sin una herramienta simple, privada y realmente útil 
para gestionar sus finanzas personales.

---

## Solucion

Capital Plus nace como una plataforma totalmente local, privada y segura, donde 
cada usuario puede almacenar y organizar su información financiera sin depender 
de terceros ni compartir datos bancarios.

El objetivo es ofrecer una herramienta clara, minimalista y centrada en lo esencial:
saber cuánto tienes, cuánto debes y cómo crece tu dinero.

---

## Logica de Negocio 

La logica de Negocio de Capital Plus se centra en 3 pilares, Ahorro, Inversion y 
Deuda.  Cada módulo sigue reglas claras para garantizar consistencia, seguridad 
y facilidad de uso.

### Gestion de Ahorro 

- Cada Ahorro se registra con:
  - La Fecha en la cual se añadio la cantidad
  - Cantidad 
- El sistema calcula:
  - El progreso del Dinero Acumulado
  - El reparto del Ahorro por meses.
  - Diferencia entre Patrimonio(Inversiones + Ahorro) y Liquidez

### Gestion de Inversion 

- Cada Inversion se registra con:
  - Identificador
  - Nombre 
  - Cantidad 
  - Precio de Compra
  - Precio de Venta
- Por otra parte tenemos un submodulo en Inversion llamado Monedas que registra:
  - Nombre 
  - Cantidad
- El sistema calcula:
  - La Ganancia total 
  - La Ganancia de una accion una vez vendida.
  - La Ganancia de una accion al dia.
  - Valor de nuestras inversiones.
  - Valor de nuestras monedas a euros(€).

### Gestion de Deudas 

- Cada deuda se registra con:
  - Identificador
  - Descripcion
  - Cantidad Total a Deber
  - Interes
  - Cantidad Pagada
- El sistema calcula:
  - Podemos visualizar que metodo queremos ver nuestras deudas (Avalnacha o Bola
    de Nieve)
  - Cuanto debemos.

---

## Seguridad y Almacenamiento

- Toda la información se guarda localmente en el dispositivo del usuario.
- No se envían datos a servidores externos.
- Cada usuario tiene su propio espacio de datos aislado.

---

## Flujo de la Aplicacion 

1. El usuario crea su perfil local.
2. Selecciona el módulo (Inversión, Ahorro o Deuda).
3. Registra la información correspondiente.
4. El sistema valida los datos.
5. Se guarda la información en almacenamiento local.
6. La app muestra resúmenes y estados actualizados.

---

## Tecnologias

- Phyton
- Sqlite

---

## Frameworks
  
- yfinance
- colorama
- tabulate
- bcrypt

---

## Instalacion

1. Bajarse el repositorio
  `git clone https://github.com/Devloy3/Capital-Plus.git`
  `cd Capital-Plus`

2. Crear un entorno 
  `python3 -m venv .venv`

3. Instalar dependencias
  `pip install -r requirements.txt`

4. Crear base de datos
  `cd Utils`
  `python3 Utils.py`
  
5. Arrancar el programa 
  `cd ..`
  `python3 main.py`
  
---

## Estado del Proyecto

Capital Plus se encuentra **terminado y completamente funcional** en su version actual.

Aun así, el proyecto seguirá evolucionando. Existen varias funcionalidades que 
se desean implementar en futuras actualizaciones, como: 

- Exportacion de toda la informacion del usuario, a un archivo.csv
- Implementacion de Machine Learning, en el que cada usuario pueda ver su finscore.
- Insertar un apartado de informacion de Hacienda
- Crear un submodulo de Capital Plus, que sea para autonomos.

Estas mejoras no afectan al funcionamiento actual, pero permitirán ampliar las capacidades de la aplicación en próximas versiones.