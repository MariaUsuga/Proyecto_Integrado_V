import datetime
import logging
import os

class Logger:
    def __init__(self):
        # Crear la carpeta logs si no existe
        if not os.path.exists('logs'):
            os.makedirs('logs')
            print("Carpeta 'logs' creada exitosamente.")
        else:
            print("La carpeta 'logs' ya existe.")

        # Nombre del archivo de log con fecha y hora
        self.log_file = f"logs/dolar_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Configuración del logger
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='[%(asctime)s | %(name)s | %(class_name)s | %(function_name)s | %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger('DolarAnalysis')

    def info(self, class_name, function_name, description):
        """Registra un mensaje de nivel INFO."""
        self.logger.info(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )

    def warning(self, class_name, function_name, description):
        """Registra un mensaje de nivel WARNING."""
        self.logger.warning(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )

    def error(self, class_name, function_name, description):
        """Registra un mensaje de nivel ERROR."""
        self.logger.error(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )
