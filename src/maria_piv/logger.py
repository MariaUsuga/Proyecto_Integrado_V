import datetime
import logging
import os

# Filtro que garantiza que siempre existan los campos extra
class ContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'class_name'):
            record.class_name = ''
        if not hasattr(record, 'function_name'):
            record.function_name = ''
        return True

class Logger:
    def __init__(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')

        self.log_file = f"logs/dolar_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='[%(asctime)s | %(name)s | %(class_name)s | %(function_name)s | %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger('DolarAnalysis')
        self.logger.addFilter(ContextFilter())  # <- importante

    def info(self, class_name, function_name, description):
        self.logger.info(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )

    def warning(self, class_name, function_name, description):
        self.logger.warning(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )

    def error(self, class_name, function_name, description):
        self.logger.error(
            description,
            extra={'class_name': class_name, 'function_name': function_name}
        )
