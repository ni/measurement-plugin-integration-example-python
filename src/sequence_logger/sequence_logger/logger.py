import logging
import functools
import inspect
import os
import traceback
import sys
from datetime import datetime

class _Logger:
    """
    A logger class to manage logging of function calls, returns, and exceptions.
    """

    def __init__(self):
        """
        Initialize the Logger instance and set up logging.
        """
        self.setup_logging()
        self.indent = 0
        self.logged_functions = set()
        self.call_stack = []

    def setup_logging(self):
        """
        Set up logging configuration, including log file creation.
        """
        log_dir = os.path.join(os.getcwd(), 'logs')  # Log in the user's home directory

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'log_{date_str}.csv')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s,%(levelname)s,%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def log(self, level: int, message: str):
        """
        Log a message with the given log level and indentation.
        """
        indent = '  ' * self.indent
        # Replace any commas in the message with semicolons to avoid breaking CSV format
        message = message.replace(',', ';')
        logging.log(level, f"{indent}{message}")

    def log_call(self, func_name: str, args: tuple, kwargs: dict, context: str, param_names: list) -> None:
        """
        Log the function call details including its arguments and context.
        """
        if not self.call_stack:
            if func_name not in self.logged_functions:
                self.logged_functions.add(func_name)
                args_repr = [f"{name}={repr(arg)}" for name, arg in zip(param_names, args)]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                self.log(logging.INFO, f"Function Call ({context}.{func_name}): {func_name}")
                self.log(logging.INFO, f"Arguments: ({signature})")
                self.indent += 1
        self.call_stack.append(func_name)

    def log_return(self, func_name: str, result):
        """
        Log the return value of a function.
        """
        if self.call_stack and self.call_stack[-1] == func_name:
            if func_name in self.logged_functions:
                self.indent -= 1
                self.log(logging.INFO, f"Return: {result!r}")
                self.log(logging.INFO, "-" * 60)
                self.logged_functions.remove(func_name)
            self.call_stack.pop()

    def log_exception(self, func_name: str, exc: Exception):
        """
        Log any exception raised within a function.
        """
        if self.call_stack and self.call_stack[-1] == func_name:
            if func_name in self.logged_functions:
                self.indent -= 1
                self.log(logging.ERROR, f"Exception in {func_name}: {exc}")
                self.log(logging.ERROR, traceback.format_exc())
                self.log(logging.INFO, "-" * 40)
                self.logged_functions.remove(func_name)
            self.call_stack.pop()

logger = _Logger()

def log_actions(func):
    """
    Decorator to log function calls, returns, and exceptions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        context = 'global'
        if args and hasattr(args[0], '__module__'):
            module_name = args[0].__module__
        else:
            module_name = func.__module__
        
        context = os.path.basename(module_name)
        
        param_names = inspect.signature(func).parameters.keys()
        logger.log_call(func.__name__, args, kwargs, context, param_names)
        try:
            result = func(*args, **kwargs)
            logger.log_return(func.__name__, result)
            return result
        except Exception as exc:
            logger.log_exception(func.__name__, exc)
            raise
    return wrapper

def apply_logging_to_module(module):
    """
    Apply logging to all functions within a specified module.
    """
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and not name.startswith('__'):
            setattr(module, name, log_actions(obj))

def apply_logging_to_all_modules():
    """
    Apply logging to all modules that match a specific pattern.
    """
    for module_name, module in sys.modules.items():
        if module_name.startswith('Clients.'):
            apply_logging_to_module(module)

def init_log():
    """
    Initialize logging for all relevant modules.
    """
    apply_logging_to_all_modules()
