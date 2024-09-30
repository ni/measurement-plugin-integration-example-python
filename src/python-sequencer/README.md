# Python Sequencer - A Reference Example

## Overview

This tool serves as a reference example for integrating the client generator and enabling the sequencing of measurement services using the generated clients. For client generation, the integration of "Measurement Service Client Generator" is required. To achieve it please refer [Client Integration](#client-integration) section.

## Steps to use the Reference Sequence tool

### Step 1: Install Poetry

Ensure Poetry is installed on your system to manage the Python environment and dependencies.

### Step 2: Run the Script

You can run the provided script `main.py` using the command line. The script allows you to either refresh clients or specify a directory where sequence files are stored.

```cli
python main.py --refresh-clients --sequence-directory /path/to/sequence/directory
```

- **--refresh-clients**: Flag to refresh or create a MeasurementLink client.
- **--sequence-directory (optional)**: Specify the directory where sequence files should be stored. Ensure the directory exists and has write permissions. (If nothing is specified then the current working directory will be assigned.)

### Step 3: Creating Clients

When the `--refresh-clients` flag is set, the script will:

1. Enumerate available Measurement services.
2. Create a client for each available service.
3. Move the created client to the specified target directory.
4. Generate or update a `custom_sequencer.py` file, which includes a start-up sequence code for the created clients.

### Step 4: Generated Sequence File

After client creation, the tool generates a `custom_sequencer.py` file with the following:

- `pin_map_methods`: A list of methods related to the client's pinmap.
- A loop that registers the pinmap for each method.
  
Users can modify this file to define their own sequences for the generated clients.

### Step 5: Logging Setup

- To ensure logging functionality across all modules, a custom logging package (`logger.py`) has been provided as a pre-built wheel package.

- Make sure to install this logging package in your sequence directory by using `pip install`. This enables the `custom_sequencer.py` file to import and utilize the logging capabilities correctly.

- Once installed, the logging package will initialize the logging configuration for the script, helping capture logs from various operations throughout the sequence.

```text
Note: Before creating clients, the tool automatically handles directory cleanup by,
    - Clearing the content of the `__init__.py` file (if it exists).
    - Removing all generated clients.
    - Deleting the `custom_sequencer.py` file (if present).
```

## Advantages

- **Client Creation**: Automatically generates clients for all active measurements.

- **Startup Code Generation**: Provides initial code in the `custom_sequencer.py` file for sequence execution, making customization easier.

- **Logging**: Logs sequencer operations, including arguments and results, to a CSV file, enhancing tracking and debugging capabilities.

- **Clean-up**: When an existing sequence directory is given, the `Clients` module and `custom_sequencer.py` file will be cleaned up and it starts generating newly.

## Disadvantages

- **Incomplete Dependency Management**: Full dependency management for the sequence directory is not yet implemented.
  - No `pyproject.toml` file has been provided with the start-up code, instead the user need to install the wheel packages *[(logger and measurement-service)](#dependencies)* manually(`pip install "path/to/wheel/package"`) in their sequence directory.

- **Reference Example**: It is not a full-fledged sequencer but rather acts as a reference example, which might require further development for production use.

## Client Integration

- Install the client generator wheel package in the cwd using `pip install "path/to/wheel/package"`.
- Import the module in the required file, i.e., `import ni_measurementlink_client.template`.
- Use methods of the client generator such as `ni_measurementlink_client.template.method_to_be_called(args)`
- Have a list  `args = ["argument1", "argument2"]` which is to be passed to the method.
- For generating client, use

    ```python
    ni_measurementlink_client.template.create_client.main(args=args)
    ```

    Here, `args` is  `[f"{client_name}", f"-m{measurement.service_class}"]` which `create_client` method expects.
    Accordingly, modify your arguments with respect to the options or the parameters that the method expects.
- Ensure that the args match with the required parameters for `create_client` method.
- For better error handling, wrap method calls inside try-except blocks to catch and log exceptions:

    ```python
    try:
        ni_measurementlink_client.template.create_client.main(args)
    except Exception as e:
        print(f"Error occurred: {e}")
    ```

## Dependencies

- **For Reference sequencer**
  - ni_measurementlink_service-1.5.0.dev4-py3-none-any.whl
  - ni_measurementlink_client-0.1.0.dev0-py3-none-any.whl
  - sequence_logger-0.1.0-py3-none-any.whl
- **For sequence execution**
  - sequence_logger-0.1.0-py3-none-any.whl
  - ni_measurementlink_service-1.5.0.dev4-py3-none-any.whl

These wheel packages has been provided in `python-sequencer\dependencies\` directory.

### Example Usage

- `python main.py --refresh-clients -s \my\sequence\directory`
    This command refreshes the clients and generates a new sequence file in the \`\my\sequence\directory\`.

- `python main.py --refresh-clients`
    This command refreshes the clients and generates a new sequence file in the current working directory.
