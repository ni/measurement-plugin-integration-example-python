# Python Sequencer - An example sequencer

## Overview

This tool serves as a reference for integrating the Measurement Plug-In Client Generator to generate measurement plug-in clients and showcase the sequencing of measurement plug-ins using the generated clients.

***Note:** Please go through the [Client Integration](/ClientIntegration.md) file before reading this document.*

## Workflow Diagram

![sequencer-example-workflow-diagram](/docs/images/sequencer-example-workflow-diagram.PNG)

## Dependencies

- **For sequencer**
  - ni-measurement-plugin-sdk-service
  - ni-measurement-plugin-sdk-generator
- **For sequence execution**
  - sequence_logger-0.1.0.dev0-py3-none-any.whl
  - ni-measurement-plugin-sdk-service

The `sequence_logger-0.1.0.dev0-py3-none-any.whl` is available in the `root\dist` directory.

## Steps to use the Sequencer tool

### Step 1: Install the Package

After downloading the `python-sequencer-x.x.x-py3-none-any.whl` wheel file, install the package using the command below.

```bash
pip install /path/to/python-sequencer-x.x.x-py3-none-any.whl
```

### Step 2: Run the Package

To run the `python-sequencer`, open your command line and enter:

```bash
python-sequencer /path/to/sequence/directory
```

- **/path/to/sequence/directory**: Specify the path to the directory where the generated clients and sequence files will be stored. Ensure that the directory exists and has write permissions.

### Step 3: Creating clients

When you run the command:

1. The tool will find all the registered measurement plug-ins.
2. It will create a client for each measurement plug-in in the specified directory.
3. It then creates a `sequence.py` file that contains the startup sequence code for the generated clients.

### Step 4: Generated Sequence File

The generated `sequence.py` file contains the following:

- `pin_map_methods`: A list of methods used to register the pin map for the measurement plug-ins, which users can update by modifying the `pin_map_path` variable.
- A loop that registers the pinmap for each method.

**Note:** Users can modify this file to define their own sequences for the generated clients.

### Step 5: Logging Setup

- A custom logger (`sequence_logger`) is provided as a package to log the execution results of the sequence.
- Make sure to install this logging package in your sequence directory by using

 ```bash
 pip install /path/to/sequence_logger-x.x.x-py3-none-any.whl
 ```

- Once installed, the logging package will initialize the logging configuration for the script, helping capture logs from various operations throughout the sequence.

```text
Note: Before creating clients, the tool automatically handles directory cleanup by,
    - Clearing the content of the `__init__.py` file (if it exists).
    - Removing all generated clients.
    - Deleting the `sequence.py` file (if present).
```

### Step 6: Execute the Sequence

- Run the `sequence.py` file to execute the sequence.
- After execution, you can find the results along with the input configurations in the log file which will be saved in the current working directory as a CSV file.

### Example Usage

- `python-sequencer /my/sequence/directory`
    This command generates new clients and a sequence file in the `/my/sequence/directory` directory.

## Merits

- **Client Creation**: Automatically generates clients for all active measurements.
- **Startup Code Generation**: Provides initial code in the `sequence.py` file for sequence execution, making customization easier.
- **Logging**: Logs sequencer operations, including arguments and results, to a CSV file, enhancing tracking and debugging capabilities.
- **Clean-up**: When an existing sequence directory is given, the `clients` module and `sequence.py` file will be cleaned up and it starts generating newly.

## Limitations

- **No Dependency Management**: Dependency management for the sequence directory is not yet implemented.
  - No `pyproject.toml` file is generated with the start-up code. Instead, the user needs to install the packages *[(logger and measurement-service)](#dependencies)* manually(`pip install "path/to/wheel/package"`) to their respective sequence directory.
