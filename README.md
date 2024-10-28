# Python Sequencer - An example sequencer

## Overview

This tool serves as a reference for integrating the Measurement Plug-In Client Generator to generate measurement plug-in clients and showcase the sequencing of measurement plug-ins using the generated clients.

***Note:** Please read [Client Integration](/ClientIntegration.md) before proceeding.*

## Workflow Diagram

![sequencer-example-workflow-diagram](/docs/images/sequencer-example-workflow-diagram.png)

## Dependencies

- **For sequencer**
  - ni-measurement-plugin-sdk-service
  - ni-measurement-plugin-sdk-generator
- **For sequence execution**
  - ni_sequence_logger-1.0.0.dev0-py3-none-any.whl
  - ni-measurement-plugin-sdk-service

The `ni_sequence_logger-1.0.0.dev0-py3-none-any.whl` is available in the `root\dist` directory.

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

### Step 3: Create the client

When you run the command:

1. The tool discovers all the registered measurement plug-ins.
2. Creates clients for each measurement plug-in and a `sequence.py` file that contains the startup sequence code that uses the clients.

### Step 4: Review the Generated Sequence File

The generated `sequence.py` file contains the following:

If the Measurement Plug-in uses the PinMap, the PinMap must be registered before every execution.

- `pin_map_methods`: A list of methods used to register the pin map for the measurement plug-ins. Update `pin_map_path` variable to the PinMap file path.
- A loop that registers the PinMap for each Measurement Plug-in.

**Note:** Users can modify this file to define their own sequences for the generated clients.

### Step 5: Set Up Logging

- A custom logger (`ni-sequence-logger`) is provided as a package to log the execution results of the sequence.
- Install this logging package using the command,

 ```bash
 pip install /path/to/ni_sequence_logger-x.x.x-py3-none-any.whl
 ```

- Once installed, the logging package will initialize the logging configuration for the script, helping capture logs from various operations throughout the sequence.

### Step 6: Execute the Sequence

- Run the `sequence.py` file to execute the sequence.
- The log will be saved as a CSV file in the current working directory.

```text
Note: Before creating clients, the tool automatically handles directory cleanup by,

- Clearing the content of the `__init__.py` file (if it exists).
- Removing all generated clients.
- Deleting the `sequence.py` file (if present).
```

### Example Usage

```bash
python-sequencer /my/sequence/directory
```

This command generates new clients and a sequence file in the `/my/sequence/directory` directory.

## Disclaimer

- **No Dependency Management**: Dependency management for the sequence directory is not implemented.
  - No `pyproject.toml` file is generated with the start-up code. Instead, the user needs to install the packages *[(logger and measurement-service)](#dependencies)* manually.
