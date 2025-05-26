# src/maria_piv/dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_grafico(csv_path, output_path='outputs/grafico_cierre.png'):
    if not os.path.exists(csv_path):
        print("El archivo de datos no existe.")
        return

    df = pd.read_csv(csv_path, parse_dates=['Date'])

    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Adj Close'], label='Cierre ajustado', color='blue')
    plt.title('Evolución del Cierre Ajustado - Acción CIB')
    plt.xlabel('Fecha')
    plt.ylabel('Precio (USD)')
    plt.grid(True)
    plt.legend()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"Gráfico guardado en: {output_path}")
