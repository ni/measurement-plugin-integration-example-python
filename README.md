# Python Sequencer - A Reference Example

## Overview

This tool serves as a reference example for integrating the measurement plug-in client generator and enabling the sequencing of measurement services using the generated clients. For generating clients for measurement plug-ins, the `ni-measurement-plugin-client-generator` is used. Please refer to the [Client Integration](#client-integration) guide for detailed instructions.

## Dependencies

- **For Reference sequencer**
  - ni-measurement-plugin-sdk-service
  - ni-measurement-plugin-sdk-generator
- **For sequence execution**
  - sequence_logger-0.1.0.dev0-py3-none-any.whl
  - ni-measurement-plugin-sdk-service

`sequence_logger-0.1.0.dev0-py3-none-any.whl` has been provided in `root\dist` directory.

## Steps to use the Reference Sequence tool

### Step 1: Install Poetry

Ensure Poetry is installed on your system to manage the Python environment and dependencies.

### Step 2: Run the Package

To run the `python-sequencer`, open your command line and enter:

```bash
python-sequencer /path/to/sequence/directory
```

- **/path/to/sequence/directory** (mandatory): The path to the directory where the generated clients and sequence files will be stored. Ensure that the directory exists and has write permissions.

### Step 3: Creating clients

When you run the command:

1. The tool will find all available measurement services.
2. It will create a client for each service in the specified directory.
3. Generate a `sequence.py` file, which includes a start-up sequence code for the created clients.

### Step 4: Generated Sequence File

After client creation, the tool generates a `sequence.py` file with the following:

- `pin_map_methods`: A list of methods related to the client's pinmap.
- A loop that registers the pinmap for each method.
Users can modify this file to define their own sequences for the generated clients.

### Step 5: Logging Setup

- To ensure logging functionality across all modules, a custom logging package (`sequence_logger`) has been provided as a package.
- Make sure to install this logging package in your sequence directory by using

 ```bash
 pip install /path/to/sequence_logger-x.x.x-py3-none-any.whl
 ```

- This enables the `sequence-logger` to be imported and utilize the logging capabilities correctly.
- Once installed, the logging package will initialize the logging configuration for the script, helping capture logs from various operations throughout the sequence.

```text
Note: Before creating clients, the tool automatically handles directory cleanup by,
    - Clearing the content of the `__init__.py` file (if it exists).
    - Removing all generated clients.
    - Deleting the `sequence.py` file (if present).
```

### Example Usage

- `python-sequencer /my/sequence/directory`
    This command generates new clients and a sequence file in the `/my/sequence/directory` directory.

## Advantages

- **Client Creation**: Automatically generates clients for all active measurements.
- **Startup Code Generation**: Provides initial code in the `sequence.py` file for sequence execution, making customization easier.
- **Logging**: Logs sequencer operations, including arguments and results, to a CSV file, enhancing tracking and debugging capabilities.
- **Clean-up**: When an existing sequence directory is given, the `clients` module and `sequence.py` file will be cleaned up and it starts generating newly.

## Disadvantages

- **Incomplete Dependency Management**: Full dependency management for the sequence directory is not yet implemented.
  - No `pyproject.toml` file has been provided with the start-up code, instead the user need to install the wheel packages *[(logger and measurement-service)](#dependencies)* manually(`pip install "path/to/wheel/package"`) in their sequence directory.

## Client Integration

- Install the client generator package in the cwd using `pip install ni-measurement-plugin-sdk-generator`.
- Import the module in the required file, i.e., `import ni_measurement_plugin_sdk_generator.client`.
- Use methods of the client generator such as `ni_measurement_plugin_sdk_generator.client.create_client.method_to_be_called(args)`
- Have a list  `args = ["argument1", "argument2"]` which is to be passed to the method.
- For generating client, use

    ```python
    ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
    ```

    Here, `args` is  

    ```python
    args = [
            f"-s{measurement.service_class}",
            f"-o{client_module_directory}",
            f"-c{class_name}",
            f"-m{module_name}",
        ]
    ```

    which `create_client` method expects.
    Accordingly, modify your arguments with respect to the options or the parameters that the method expects.
- Ensure that the args match with the required parameters for `create_client` method.
- For better error handling, wrap method calls inside try-except blocks to catch and log exceptions:

    ```python
    try:
        ni_measurement_plugin_sdk_generator.client.create_client.main(args=args)
    except Exception as e:
        print(f"Error occurred: {e}")
    ```
