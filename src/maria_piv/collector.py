import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

class Collector:
    def __init__(self, logger):
        self.url = 'https://es.finance.yahoo.com/quote/CIB/history/'
        self.logger = logger

        os.makedirs('src/maria_piv/static/data', exist_ok=True)

    def collertor_data(self):
        try:
            df = pd.DataFrame()
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }

            response = requests.get(self.url, headers=headers)
            if response.status_code != 200:
                self.logger.error("Collector", "collertor_data", f"Error al consultar la URL: {response.status_code}")
                return df

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None:
                self.logger.error("Collector", "collertor_data", "No se encontró la tabla con los datos históricos.")
                return df

            headers_table = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []

            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(headers_table):
                    rows.append(columns)

            df = pd.DataFrame(rows, columns=headers_table).rename(columns={
                'Fecha': 'fecha',
                'Abrir': 'abrir',
                'Máx.': 'max',
                'Mín.': 'min',
                'CerrarPrecio de cierre ajustado para splits.': 'cerrar',
                'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.': 'cierre_ajustado',
                'Volumen': 'volumen'
            })

            self.logger.info("Collector", "collertor_data", f"Datos obtenidos exitosamente: {df.shape}")
            return df

        except Exception as error:
            self.logger.error("Collector", "collertor_data", f"Excepción al obtener los datos: {error}")
            return pd.DataFrame()
