import logging
from logging.handlers import RotatingFileHandler

log_file = 'log/users.log'
all_log_file = 'log/all.log'

logging.basicConfig(
        filename='log/all.log',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        level=logging.DEBUG
)

# Handler for rotating based on size
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=134217728,  # 128 MB
    backupCount=3,
)
handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))


# Add the handler to the logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)

