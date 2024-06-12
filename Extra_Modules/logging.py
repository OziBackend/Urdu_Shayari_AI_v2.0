import logging

class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def get_logger():
    # Create logger
    logger = logging.getLogger('multi_file_logger')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    success_handler = logging.FileHandler('success.log', encoding='utf-8')
    failure_handler = logging.FileHandler('failure.log', encoding='utf-8')
    prompts_handler = logging.FileHandler('prompts.log', encoding='utf-8')

    # Create filters
    success_filter = LevelFilter(logging.INFO)
    failure_filter = LevelFilter(logging.ERROR)
    prompts_filter = LevelFilter(logging.DEBUG)

    # Set levels for handlers
    success_handler.setLevel(logging.INFO)
    failure_handler.setLevel(logging.ERROR)
    prompts_handler.setLevel(logging.DEBUG)

    # Add filters to handlers
    success_handler.addFilter(success_filter)
    failure_handler.addFilter(failure_filter)
    prompts_handler.addFilter(prompts_filter)

    # Create formatters and add them to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    success_handler.setFormatter(formatter)
    failure_handler.setFormatter(formatter)
    prompts_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(success_handler)
    logger.addHandler(failure_handler)
    logger.addHandler(prompts_handler)

    return logger