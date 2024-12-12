import logging

# Normal information and warnings logger
info_logger = logging.getLogger("info_logger")
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler("info.log", encoding="utf-8")
info_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                 datefmt='%m/%d/%Y %I:%M:%S %p')
info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)

# Errors logger
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler("error.log", encoding="utf-8")
error_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                 datefmt='%m/%d/%Y %I:%M:%S %p')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

# System health logger
health_logger = logging.getLogger("health_logger")
health_logger.setLevel(logging.INFO)
health_handler = logging.FileHandler("health.log", encoding="utf-8")
health_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                 datefmt='%m/%d/%Y %I:%M:%S %p')
health_handler.setFormatter(health_formatter)
health_logger.addHandler(health_handler)
