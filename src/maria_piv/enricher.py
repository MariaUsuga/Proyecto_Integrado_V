import numpy as np
import pandas as pd

class Enricher:
    def __init__(self, logger=None):
        self.logger = logger

    def formatear_fechas(self, df=pd.DataFrame()):
        try:
            df = df.copy()
            if 'fecha' not in df.columns:
                msg = "La columna 'fecha' no existe en el DataFrame."
                if self.logger:
                    self.logger.error('Enricher', 'formatear_fechas', msg)
                else:
                    print("ERROR:", msg)
                return pd.DataFrame()

            # Convierte la columna 'fecha' a datetime, asume formato día primero
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', dayfirst=True)

            if self.logger:
                self.logger.info('Enricher', 'formatear_fechas', 'Columna fecha formateada correctamente')
            return df
        except Exception as e:
            msg = f'Error al formatear fechas: {e}'
            if self.logger:
                self.logger.error('Enricher', 'formatear_fechas', msg)
            else:
                print("ERROR:", msg)
            return pd.DataFrame()

    def calcular_kpi(self, df=pd.DataFrame()):
        try:
            df = df.copy()
            if 'fecha' not in df.columns:
                msg = "La columna 'fecha' no existe en el DataFrame."
                if self.logger:
                    self.logger.error('Enricher', 'calcular_kpi', msg)
                else:
                    print("ERROR:", msg)
                return pd.DataFrame()

            df = df.sort_values('fecha')

            for col in df.columns:
                if col != "fecha":
                    if df[col].dtype == 'object':
                        # Reemplaza coma por punto solo si la columna es string
                        df[col] = pd.to_numeric(df[col].str.replace(',', '.', regex=False), errors='coerce')

            # Calcula volatilidad como desviación estándar rolling 5 días
            if 'cerrar' in df.columns:
                df['volatilidad'] = df['cerrar'].rolling(window=5).std().fillna(0)
            else:
                msg = "La columna 'cerrar' no existe en el DataFrame, no se puede calcular volatilidad."
                if self.logger:
                    self.logger.warning('Enricher', 'calcular_kpi', msg)
                else:
                    print("WARNING:", msg)
                df['volatilidad'] = np.nan

            if self.logger:
                self.logger.info('Enricher', 'calcular_kpi', 'Agregados indicadores KPI')
            return df
        except Exception as errores:
            msg = f'Error al enriquecer el df: {errores}'
            if self.logger:
                self.logger.error('Enricher', 'calcular_kpi', msg)
            else:
                print("ERROR:", msg)
            return pd.DataFrame()
