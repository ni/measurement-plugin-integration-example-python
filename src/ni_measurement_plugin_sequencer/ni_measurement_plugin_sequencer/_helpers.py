import ast
import pathlib
import re
from typing import Any, Dict, List, Optional, Tuple

import click
import ni_measurement_plugin_sdk_generator.client
import ni_measurement_plugin_sdk_generator.client.templates
from mako.template import Template
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient

_V2_MEASUREMENT_SERVICE_INTERFACE = "ni.measurementlink.measurement.v2.MeasurementService"
# List of regex patterns to convert camel case to snake case
_CAMEL_TO_SNAKE_CASE_REGEXES = [
    re.compile("([^_\n])([A-Z][a-z]+)"),
    re.compile("([a-z])([A-Z])"),
    re.compile("([0-9])([^_0-9])"),
    re.compile("([^_0-9])([0-9])"),
]


def _get_function_parameters(node: ast.FunctionDef) -> Dict[str, str]:
    """Extracts function parameters and their default values from an AST node."""
    func_params: Dict[str, str] = {}

    # Iterate through the function's arguments, adding them to the func_params dictionary.
    for arg in node.args.args:
        # Ignore 'self' as it is used for instance methods in classes and is not needed here.
        if arg.arg != "self":
            func_params[arg.arg] = ""

    # Match default values to parameters from right to left in the parameter list
    for i, default in enumerate(node.args.defaults):
        # "-len(node.args.defaults) + i" gives us the correct index from the end of the list
        arg_name = node.args.args[-len(node.args.defaults) + i].arg
        func_params[arg_name] = _get_default_value_as_str(default)

    return func_params


def _get_default_value_as_str(default: ast.AST) -> str:
    """Parses the default value of a function parameter from its AST node."""
    if isinstance(default, ast.Constant):
        return str(default.value)
    if isinstance(default, ast.List):
        return str([elem.value for elem in default.elts if isinstance(elem, ast.Constant)])
    if isinstance(default, ast.Dict):
        return str(
            {
                k.value: v.value
                for k, v in zip(default.keys, default.values)
                if isinstance(k, ast.Constant) and isinstance(v, ast.Constant)
            }
        )
    return ""


def _remove_suffix(string: str) -> str:
    """Removes known suffixes from a string."""
    suffixes = ["_Python", "_LabVIEW"]
    for suffix in suffixes:
        if string.endswith(suffix):
            return string.removesuffix(suffix)
    return string


def _extract_base_service_class(service_class: str) -> str:
    """Creates a base service class from the measurement service class."""
    base_service_class = service_class.split(".")[-1]
    base_service_class = _remove_suffix(base_service_class)

    if not base_service_class.isidentifier():
        raise click.ClickException(
            f"Client creation failed for '{service_class}'.\nEither provide a module name or update the measurement with a valid service class."
        )
    if not any(ch.isupper() for ch in base_service_class):
        print(
            f"Warning: The service class '{service_class}' does not adhere to the recommended format."
        )
    return base_service_class


def _camel_to_snake_case(camel_case_string: str) -> str:
    """Converts a camel case string to snake case."""
    partial = camel_case_string
    for regex in _CAMEL_TO_SNAKE_CASE_REGEXES:
        partial = regex.sub(r"\1_\2", partial)

    return partial.lower()


def _create_module_name(base_service_class: str) -> str:
    """Creates a module name using a base service class."""
    return _camel_to_snake_case(base_service_class) + "_client"


def _create_class_name(base_service_class: str) -> str:
    """Creates a class name using a base service class."""
    return base_service_class.replace("_", "") + "Client"


def _clear_file(file_path: pathlib.Path) -> None:
    """Clears the content of a file."""
    open(file_path, "w").close()


def _delete_file(file_path: pathlib.Path) -> None:
    """Deletes a file if it exists."""
    if file_path.is_file():
        file_path.unlink(missing_ok=True)


def _render_template(template_name: str, **template_args: Any) -> bytes:
    """Renders the Mako template and returns the output as bytes."""
    template_file_path = str(pathlib.Path(__file__).parent / "templates" / template_name)
    template = Template(
        filename=template_file_path,
        input_encoding="utf-8",
        output_encoding="utf-8",
        default_filters=["n"],
    )
    return template.render(**template_args)


def _create_new_sequence_file(file_path: pathlib.Path, **template_args: Any) -> None:
    """Writes a new Python file that initializes logging and registers pinmap methods."""
    try:
        rendered_content = _render_template("sequence.py.mako", **template_args)
    except Exception as e:
        raise click.ClickException(f"An error occurred while rendering the template: {str(e)}")

    with open(file_path, "wb") as file:
        file.write(rendered_content)

    print(f"File created and sequence list written to {file_path}")


def analyze_functions_and_parameters(
    file_path: pathlib.Path,
) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
    """Analyze a Python file to extract method names and their parameters.

    This method parses a Python file and retrieves all function definitions along
    with their parameters and default values.

    Args:
        file_path: The path to the Python file to analyze.

    Returns:
        A tuple containing:
        - A list of method names.
        - A dictionary mapping method names to their parameters and default values.

    Raises:
        FileNotFoundError: If the file cannot be found.
        SyntaxError: If there is an issue parsing the Python file.
    """
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    methods: List[str] = []
    params: Dict[str, Dict[str, str]] = {}

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and not node.name.startswith("_")
            and not node.decorator_list
        ):
            methods.append(node.name)
            func_params = _get_function_parameters(node)
            params[node.name] = func_params

    return methods, params


def clean_up(user_directory: pathlib.Path) -> None:
    """Delete files in the clients directory and remove the sequence.py file.

    This method cleans up files in the given directory by removing all files within
    the clients subdirectory and deleting the sequence.py file if it exists.

    Args:
        user_directory: The path to the user directory containing the clients directory
                        and sequence.py file.

    Raises:
        FileNotFoundError: If the directory or files do not exist.
    """
    client_directory = user_directory / "clients"
    for filename in client_directory.iterdir():
        file_path = client_directory / filename
        _delete_file(file_path)

    sequencer_path = user_directory / "sequence.py"
    _delete_file(sequencer_path)


def configure_init_file(
    client_module_directory: pathlib.Path,
    list_of_class_names: List[str],
    list_of_module_names: List[str],
) -> None:
    """Configure the __init__.py file for the client module.

    This method creates or updates the __init__.py file in the client module
    directory by importing the necessary class names from their respective modules.

    Args:
        client_module_directory: The directory where the client module is located.
        list_of_class_names: List of class names to be imported in the __init__.py file.
        list_of_module_names: List of module names corresponding to the class names.

    Raises:
        FileNotFoundError: If the client module directory does not exist.
    """
    init_content: List[str] = []

    for module_name, class_name in zip(list_of_module_names, list_of_class_names):
        init_content.append(f"from clients.{module_name} import {class_name}")
    init_content.append("")

    for module_name, class_name in zip(list_of_module_names, list_of_class_names):
        init_content.append(f"{module_name} = {class_name}()")

    init_file_text: str = "\n".join(init_content)
    init_file_path = client_module_directory / "__init__.py"

    with open(init_file_path, "w") as init_file:
        init_file.write(init_file_text)

    print(f"__init__.py file has been created at: {init_file_path}")


def write_sequence_file(
    list_of_client_directories: List[pathlib.Path],
    user_directory: pathlib.Path,
    list_of_module_names: List[str],
) -> None:
    """Write a sequence file based on client directories and class names.

    This method writes a new Python file called sequence.py based on the
    provided client directories and class names.

    Args:
        list_of_client_directories: A list of paths to client directories containing the
                                    necessary modules.
        user_directory: The path to the user directory where the sequence.py
                        file will be written.
        list_of_module_names: List of module names to be included in the sequence file.

    Raises:
        FileNotFoundError: If the provided directory paths do not exist.
    """
    methods, _ = analyze_functions_and_parameters(
        list_of_client_directories[0]
    )  # assuming all clients have the same methods
    pinmap_methods: List[str] = [f"{func}" for func in methods if "pin" in func.lower()]
    _create_new_sequence_file(
        file_path=user_directory / "sequence.py",
        instance_names=[client for client in list_of_module_names],
        callables=pinmap_methods,
    )


def create_client(target_path: Optional[pathlib.Path] = None) -> None:
    """Create a client and generate the required configuration files.

    This method creates a client by generating necessary files, configuring
    the client directory, and cleaning up any pre-existing files.

    Args:
        target_path: The target directory for the client creation. If not specified,
                     the current working directory will be used.

    Raises:
        FileNotFoundError: If the target directory does not exist.
        Exception: If client generation fails for any reason.
    """
    user_directory = pathlib.Path(target_path if target_path is not None else pathlib.Path.cwd())
    client_module_directory = user_directory / "clients"

    if not client_module_directory.exists():
        client_module_directory.mkdir(parents=True, exist_ok=True)

    list_of_client_directories: List[pathlib.Path] = []
    list_of_class_names: List[str] = []
    list_of_module_names: List[str] = []

    discovery_client = DiscoveryClient()
    available_measurement_services = discovery_client.enumerate_services(
        _V2_MEASUREMENT_SERVICE_INTERFACE
    )

    clean_up(user_directory=user_directory)

    for measurement in available_measurement_services:
        base_service_class = _extract_base_service_class(measurement.service_class)
        class_name = _create_class_name(base_service_class)
        module_name = _create_module_name(base_service_class)
        args = [
            f"-s{measurement.service_class}",
            f"-o{client_module_directory}",
            f"-c{class_name}",
            f"-m{module_name}",
        ]
        try:
            ni_measurement_plugin_sdk_generator.client.create_client(args=args)
        except SystemExit as e:
            if e.code != 0:
                continue
        except Exception as e:
            raise Exception("Exception thrown from client generation: ", e)

        client_directory = client_module_directory / f"{module_name}.py"
        list_of_client_directories.append(client_directory)
        list_of_class_names.append(class_name)
        list_of_module_names.append(module_name)

    configure_init_file(
        client_module_directory=client_module_directory,
        list_of_class_names=list_of_class_names,
        list_of_module_names=list_of_module_names,
    )

    write_sequence_file(
        list_of_client_directories=list_of_client_directories,
        list_of_module_names=list_of_module_names,
        user_directory=user_directory,
    )
