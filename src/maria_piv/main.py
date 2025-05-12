from logger import Logger
from collector import Collector
from enricher import Enricher
import pandas as pd


def main():
    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)
    enricher = Enricher(logger=logger)
    
    df =collector.collertor_data()
    df.to_csv("src/maria_piv/static/data/dolar_data.csv")
    df_2=enricher.calcular_kpi(df)
    df_2.to_csv("src/maria_piv/static/data/dolar_data_enricher.csv")





if __name__ == "__main__":
    main()