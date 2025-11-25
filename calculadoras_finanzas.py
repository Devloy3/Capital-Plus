class Finanzas:
    @staticmethod
    def desglose_de_ahorro(monto,años,inflacion):

        meses_totales = 12 * años
        cuantia_total = meses_totales * monto
        decimal = inflacion / 100
        inflacion_acumulada = (1+float(decimal))** años-1
        monto_real = float(cuantia_total) / (1+float(inflacion_acumulada))

        return monto_real,cuantia_total,años
    
    @staticmethod
    def administracion_de_dinero(salario):
        
        MITAD = float(salario) * 0.50
        PARTE1 = float(salario) * 0.30 
        PARTE2 = float(salario) * 0.20

        texto = f'''
                Dinero destinado a casa: {int(MITAD)}€
                Dinero para mis gastos propios: {int(PARTE1)}€
                Dinero para ahorro i inversion: {int(PARTE2)}€
                '''
    
        return texto
    
    @staticmethod
    def desglose_gastos(ingresos,gastos):
        RESULTADO = ingresos-gastos

        texto = (f'''
              Ingresos: {ingresos}€
              Gastos: {gastos}€
              -------------------------
              Resultado: {int(RESULTADO)}€
              ''')
        
        return texto
        

    
    