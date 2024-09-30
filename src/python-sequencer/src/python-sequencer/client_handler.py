import ast
import pathlib
from typing import Dict, List, Optional, Tuple

import ni_measurement_plugin_sdk_generator.client
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient

_V2_MEASUREMENT_SERVICE_INTERFACE = "ni.measurementlink.measurement.v2.MeasurementService"


def _get_function_parameters(node: ast.FunctionDef) -> Dict[str, str]:
    """
    Extract the parameters of a function from its AST node.
    """
    func_params: Dict[str, str] = {}

    # Iterate through the function's arguments, adding them to the func_params dictionary.
    for arg in node.args.args:
        # Ignore 'self' as it is typically used for instance methods in classes and is not needed here.
        if arg.arg != "self":
            func_params[arg.arg] = ""

    # Match default values to parameters from right to left in the parameter list
    for i, default in enumerate(node.args.defaults):
        # "-len(node.args.defaults) + i" gives us the correct index from the end of the list
        arg_name = node.args.args[-len(node.args.defaults) + i].arg
        func_params[arg_name] = _get_default_value(default)

    return func_params


def _get_default_value(default: ast.AST) -> str:
    """
    Parse the default value of a function parameter from its AST node.
    """
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


def _get_last_segment_from_string(input_string: str, delimiter: str = ".") -> str:
    """
    Extracts the last segment of a string that is divided by a specified delimiter.
    """
    segments = input_string.split(delimiter)
    return segments[-1]


def _clear_file(file_path: pathlib.Path) -> None:
    """
    Helper function to clear the content of a file.
    """
    with open(file_path, "w") as file:
        file.write("")


def _delete_file(file_path: pathlib.Path) -> None:
    """
    Helper function to delete a file.
    """
    file_path = pathlib.Path(file_path)
    if file_path.is_file():
        file_path.unlink()


def _create_new_sequence_file(
    file_path: pathlib.Path, instance_names: List[str], callables: List[str]
) -> None:
    """
    Write a new Python file that initializes logging and registers pinmap methods.

    Args:
        file_path (pathlib.Path): The path where the new file will be created.
        client_name (str): The name of the client to be used in the file.
        callables (List[str]): A list of callable method names to be included in the pin_map_methods.

    Returns:
        None
    """
    import_instances = ", ".join(instance_names)
    sequence_file_content = []

    sequence_file_content.append(f"from Clients import {import_instances}\n")
    sequence_file_content.append("from sequence_logger import init_log\n\n")
    sequence_file_content.append("init_log()\n\n")
    sequence_file_content.append("pin_map_methods = [\n")

    for instance_name in instance_names:
        for func in callables:
            sequence_file_content.append(f"    {instance_name}.{func},\n")

    sequence_file_content.append("\n]\n")
    sequence_file_content.append(
        'pin_map_path = r"path\\to\\pinmap\\file"  # update your pinmap path here\n\n'
    )
    sequence_file_content.append("# pinmap will be registered to all the instruments\n")
    sequence_file_content.append("for register_pin_map in pin_map_methods:\n")
    sequence_file_content.append("    register_pin_map(pin_map_path)\n\n")
    sequence_file_content.append("# write your sequence here\n")

    # Write all content to the file at once
    with open(file_path, "w") as file:
        file.write("".join(sequence_file_content))

        print(f"File created and sequence list written to {file_path}")


def analyze_functions_and_parameters(
    file_path: pathlib.Path,
) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
    """
    Analyze a Python file to extract method names and their parameters.

    Args:
        file_path (pathlib.Path): The path to the Python file to analyze.

    Returns:
        Tuple[List[str], Dict[str, Dict[str, str]]]: A tuple containing:
            - A list of method names.
            - A dictionary where keys are method names and values are dictionaries of parameter names and their default values.
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
    """
    Deletes all files in the Clients directory and removes the custom_sequencer.py file.

    Args:
        user_directory (pathlib.Path): The path to the user directory where the Clients
                                        directory and custom_sequencer.py file are located.

    Returns:
        None
    """
    user_directory = pathlib.Path(user_directory)
    client_directory = user_directory / "Clients"
    # Delete all files in the Clients directory
    for filename in client_directory.iterdir():
        file_path = client_directory / filename
        _delete_file(file_path)

    # Delete custom_sequencer.py
    sequencer_path = user_directory / "custom_sequencer.py"
    _delete_file(sequencer_path)


def configure_init_file(
    client_module_directory: pathlib.Path,
    list_of_class_names: List[str],
    list_of_module_names: List[str],
) -> None:
    """
    Configure the __init__.py file in the given module directory.

    Args:
        client_module_directory (pathlib.Path): The directory for the client module.
        list_of_class_names (List[str]): List of class names to be imported.
        list_of_module_names (List[str]): List of module names corresponding to the class names.

    Returns:
        None
    """
    init_content: List[str] = []

    for module_name, class_name in zip(list_of_module_names, list_of_class_names):
        init_content.append(f"from {module_name} import {class_name}")
    init_content.append("")

    for class_name in list_of_class_names:
        init_content.append(f"{class_name.lower()} = {class_name}()")

    init_content = "\n".join(init_content)
    init_file_path = client_module_directory / "__init__.py"

    with open(init_file_path, "w") as init_file:
        init_file.write(init_content)

    print(f"__init__.py file has been created at: {init_file_path}")


def write_sequence_file(
    list_of_client_directories: List[pathlib.Path],
    user_directory: pathlib.Path,
    list_of_class_names: List[str],
) -> None:
    """
    Write a sequence file based on the provided client directories and class names.

    Args:
        list_of_client_directories (List[pathlib.Path]): List of client directory paths.
        user_directory (pathlib.Path): The user directory where the sequence file will be written.
        list_of_class_names (List[str]): List of class names to be included.

    Returns:
        None
    """
    methods, _ = analyze_functions_and_parameters(
        list_of_client_directories[0]
    )  # passing the first client as all clients has the same methods
    pinmap_methods: List[str] = [f"{func}" for func in methods if "pin" in func.lower()]
    _create_new_sequence_file(
        file_path=user_directory / "custom_sequencer.py",
        instance_names=[client.lower() for client in list_of_class_names],
        callables=pinmap_methods,
    )


def create_client(target_path: Optional[pathlib.Path] = None) -> None:
    """
    Create a client by generating necessary files and configurations.

    Args:
        target_path (Optional[pathlib.Path]): The target directory for client creation. Defaults to current working directory.

    Returns:
        None
    """
    if not target_path:
        user_directory = pathlib.Path.cwd()
    else:
        user_directory: pathlib.Path = target_path
    client_module_directory = user_directory / "Clients"

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
        class_name = _get_last_segment_from_string(measurement.service_class)
        module_name = _get_last_segment_from_string(measurement.service_class + "_client")
        args = [
            f"-s{measurement.service_class}",
            f"-o{client_module_directory}",
            f"-c{class_name}",
            f"-m{module_name}",
        ]
        try:
            ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
        except SystemExit:
            pass
        except Exception as e:
            print("Exception thrown from client generation: ", e)

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
        list_of_class_names=list_of_class_names,
        list_of_client_directories=list_of_client_directories,
        user_directory=user_directory,
    )
