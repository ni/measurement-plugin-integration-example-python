import functools
import inspect
import logging
import os
import sys
import traceback
from datetime import datetime


class _Logger:
    """
    A logger class to manage logging of instance method calls, returns, and exceptions.
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
        log_dir = os.path.join(os.getcwd(), "logs")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"log_{date_str}.csv")

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s,%(levelname)s,%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def log(self, level: int, message: str):
        """
        Log a message with the given log level and indentation.
        """
        indent = "  " * self.indent
        message = message.replace(",", ";")
        logging.log(level, f"{indent}{message}")

    def log_call(
        self, instance, method_name: str, args: tuple, kwargs: dict, context: str, param_names: list
    ) -> None:
        """
        Log the instance method call details including its arguments and context.
        """
        call_signature = f"{instance.__class__.__name__}.{method_name}"

        if not self.call_stack:
            if call_signature not in self.logged_functions:
                self.logged_functions.add(call_signature)
                # Skip 'self' in param names and args
                args_repr = [
                    f"{name}={repr(arg)}" for name, arg in zip(list(param_names)[1:], args[1:])
                ]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                self.log(logging.INFO, f"Method Call: {call_signature}")
                self.log(logging.INFO, f"Arguments: ({signature})")
                self.indent += 1

        self.call_stack.append(call_signature)

    def log_return(self, instance, method_name: str, result):
        """
        Log the return value of an instance method.
        """
        call_signature = f"{instance.__class__.__name__}.{method_name}"
        if self.call_stack and self.call_stack[-1] == call_signature:
            if call_signature in self.logged_functions:
                self.indent -= 1
                self.log(logging.INFO, f"Return: {result!r}")
                self.log(logging.INFO, "-" * 80)
                self.logged_functions.remove(call_signature)
            self.call_stack.pop()

    def log_exception(self, instance, method_name: str, exc: Exception):
        """
        Log any exception raised within an instance method.
        """
        call_signature = f"{instance.__class__.__name__}.{method_name}"
        if self.call_stack and self.call_stack[-1] == call_signature:
            if call_signature in self.logged_functions:
                self.indent -= 1
                self.log(logging.ERROR, f"Exception in {call_signature}: {exc}")
                self.log(logging.ERROR, traceback.format_exc())
                self.log(logging.INFO, "-" * 40)
                self.logged_functions.remove(call_signature)
            self.call_stack.pop()


logger = _Logger()


def log_instance_method(func):
    """
    Decorator to log instance method calls, returns, and exceptions.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if this is an instance method call
        if not args or not hasattr(args[0], "__class__"):
            # This is not an instance method call, just return without logging
            return func(*args, **kwargs)

        instance = args[0]
        if instance.__class__.__module__ == "__main__":
            # Skip logging for instances from the main module
            return func(*args, **kwargs)

        context = os.path.basename(instance.__class__.__module__)
        param_names = list(inspect.signature(func).parameters.keys())

        logger.log_call(instance, func.__name__, args, kwargs, context, param_names)
        try:
            result = func(*args, **kwargs)
            logger.log_return(instance, func.__name__, result)
            return result
        except Exception as exc:
            logger.log_exception(instance, func.__name__, exc)
            raise

    return wrapper


def apply_logging_to_class(cls):
    """
    Apply logging to all methods of a class.
    """
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("__"):
            setattr(cls, name, log_instance_method(method))
    return cls


def apply_logging_to_module(module):
    """
    Apply logging to all classes within a specified module.
    """
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            apply_logging_to_class(obj)


def apply_logging_to_all_modules():
    """
    Apply logging to all modules that match a specific pattern.
    """
    for module_name, module in sys.modules.items():
        if module_name.startswith("Clients."):
            apply_logging_to_module(module)


def init_log():
    """
    Initialize logging for all relevant modules.
    """
    apply_logging_to_all_modules()
