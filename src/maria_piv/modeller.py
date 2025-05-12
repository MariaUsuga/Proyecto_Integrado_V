import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class Modeller:
    def __init__(self, logger):
        self.logger = logger
        self.model_ruta = "src/maria_piv/static/models/"
        self.pkl_ruta = os.path.join(self.model_ruta, "dolar_model.pkl")

        if not os.path.exists(self.model_ruta):
            os.makedirs(self.model_ruta)
            self.logger.info("Modeller", "__init__", f"Carpeta {self.model_ruta} creada")

        self.model = None

    def preparar_df(self, df=pd.DataFrame()):
        try:
            df = df.copy()
            df = df.sort_values('fecha')
            df = df.dropna(subset=['cerrar', 'volatilidad'])

            # Convertir a float si aún es string
            df['cerrar'] = pd.to_numeric(df['cerrar'], errors='coerce')
            df['volatilidad'] = pd.to_numeric(df['volatilidad'], errors='coerce')

            df = df.dropna()

            X = df[['volatilidad']]
            y = df['cerrar']

            self.logger.info("Modeller", "preparar_df", "Datos preparados correctamente")

            return X, y, True
        except Exception as e:
            self.logger.error("Modeller", "preparar_df", f"Error al preparar datos: {e}")
            return pd.DataFrame(), pd.Series(), False

    def entrenar_df(self, X, y):
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = LinearRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            self.logger.info("Modeller", "entrenar_df", f"Modelo entrenado - MSE: {mse:.2f}, R2: {r2:.2f}")

            with open(self.pkl_ruta, 'wb') as f:
                pickle.dump(model, f)
                self.logger.info("Modeller", "entrenar_df", "Modelo guardado como dolar_model.pkl")

            self.model = model
            return model, True
        except Exception as e:
            self.logger.error("Modeller", "entrenar_df", f"Error al entrenar el modelo: {e}")
            return None, False

    def predecir_df(self, df=pd.DataFrame()):
        try:
            if self.model is None:
                with open(self.pkl_ruta, 'rb') as f:
                    self.model = pickle.load(f)
                    self.logger.info("Modeller", "predecir_df", "Modelo cargado desde archivo")

            df = df.copy()
            df['volatilidad'] = pd.to_numeric(df['volatilidad'], errors='coerce')
            df = df.dropna(subset=['volatilidad'])

            df['prediccion'] = self.model.predict(df[['volatilidad']])

            ultima_fecha = df['fecha'].iloc[-1]
            valor_predicho = df['prediccion'].iloc[-1]

            self.logger.info("Modeller", "predecir_df", f"Predicción realizada para {ultima_fecha}: {valor_predicho:.2f}")

            return df, True, valor_predicho, ultima_fecha, df.shape[0]
        except Exception as e:
            self.logger.error("Modeller", "predecir_df", f"Error al predecir: {e}")
            return pd.DataFrame(), False, 0, "", 0
