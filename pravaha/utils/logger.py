import logging

class Logger:
    def __init__(self, original_function):
        logging.basicConfig(filename=f'{original_function.__name__}.log', level=logging.INFO)
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        logging.info(f"Function named: {self.original_function.__name__} ran with args: {args} and kwargs: {kwargs}")
        return self.original_function(*args, **kwargs)