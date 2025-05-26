import os
import pandas as pd
from logger import Logger
from collector import Collector
from enricher import Enricher
from dashboard import dashboard

def main():
    logger = Logger()
    logger.info('Main', 'main', 'Inicializar clase Logger')

    # Crear carpeta si no existe
    os.makedirs("src/maria_piv/static/data", exist_ok=True)

    collector = Collector(logger=logger)
    enricher = Enricher(logger=logger)

    # Recolección de datos
    df = collector.collector_data()
    raw_data_path = "src/maria_piv/static/data/dolar_data.csv"
    df.to_csv(raw_data_path, index=False)
    logger.info('Main', 'main', f'Datos recolectados guardados en {raw_data_path}')

    # Enriquecimiento
    df_enriched = enricher.calcular_kpi(df)
    enriched_data_path = "src/maria_piv/static/data/dolar_data_enricher.csv"
    df_enriched.to_csv(enriched_data_path, index=False)
    logger.info('Main', 'main', f'Datos enriquecidos guardados en {enriched_data_path}')

    # Generación de gráfico
    dashboard.generar_grafico(enriched_data_path)
    logger.info('Main', 'main', f'Gráfico generado desde {enriched_data_path}')


if __name__ == "__main__":
    main()
