from collector import Collector
from enricher import Enricher
from modeller import Modeller
import pandas as pd


def main():
    logger = Logger()
    logger.info('Main', 'main', 'Inicializar logger')

    try:
        # Inicializar clases
        collector = Collector(logger=logger)
        enricher = Enricher(logger=logger)
        modeller = Modeller(logger=logger)

        # Recolectar datos
        df = collector.collertor_data()
        if df.empty:
            logger.warning("Main", "main", "El DataFrame recolectado está vacío.")
            return

        df.to_csv("src/maria_piv/static/data/dolar_data.csv", index=False)
        logger.info("Main", "main", "Datos guardados en dolar_data.csv")

        # Enriquecer datos
        df_enriched = enricher.calcular_kpi(df)
        if df_enriched.empty:
            logger.warning("Main", "main", "No se pudieron enriquecer los datos.")
            return

        df_enriched.to_csv("src/maria_piv/static/data/dolar_data_enricher.csv", index=False)
        logger.info("Main", "main", "Datos enriquecidos guardados en dolar_data_enricher.csv")

        # Modelar y predecir
        X, y, ok = modeller.preparar_df(df_enriched)
        if not ok:
            logger.warning("Main", "main", "Preparación de datos fallida.")
            return

        model, entrenado = modeller.entrenar_df(X, y)
        if not entrenado:
            logger.warning("Main", "main", "Entrenamiento del modelo fallido.")
            return

        df_pred, ok, valor, fecha, fila = modeller.predecir_df(df_enriched)
        if not ok:
            logger.warning("Main", "main", "Predicción fallida.")
            return

        df_pred.to_csv("src/maria_piv/static/data/dolar_data_predicciones.csv", index=False)
        logger.info("Main", "main", f"Predicciones guardadas. Última predicción: {valor:.2f} en {fecha}")

    except Exception as e:
        logger.error("Main", "main", f"Error general en main: {e}")


if __name__ == "__main__":
    main()
