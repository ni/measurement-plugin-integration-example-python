# An Example Measurement Plug-In Sequencer for Python

## Overview

This tool serves as a reference for integrating the Measurement Plug-In Client Generator to generate measurement plug-in clients and showcase the sequencing of measurement plug-ins using the generated clients.

***Note:** Please read [Measurement Plug-In Client Integration](/docs/Measurement%20Plug-In%20Client%20Integration.md) before proceeding.*

## Workflow Diagram

![sequencer-example-workflow-diagram](./docs/images/sequencer-example-workflow-diagram.png)

## Dependencies

- Python 3.9 or later
- The Measurement Plug-In Sequencer depends on:
  - ni-measurement-plugin-sdk-service
  - ni-measurement-plugin-sdk-generator
- To execute the generated sequence, the following dependency is required:
  - ni_sequence_logger

Please download the `ni_sequence_logger-x.x.x-py3-none-any.whl` file from the latest release assets.

## Steps to use the Sequencer tool

### Step 1: Install the Package

After downloading the `ni_measurement_plugin_sequencer-x.x.x-py3-none-any.whl` wheel file, install the package using the command below.

```bash
pip install <path_to_ni_measurement_plugin_sequencer-x.x.x-py3-none-any.whl>
```

### Step 2: Run the Sequencer

To run the `ni-measurement-plugin-sequencer`, open your command line and enter:

```bash
ni-measurement-plugin-sequencer <path_to_sequence_directory>
```

- **<path_to_sequence_directory>**: Specify the directory path where the generated clients and sequence files will be stored. Confirm that the directory exists and has the necessary write permissions.

### Step 3: Review the Generated Sequence File

The generated `sequence.py` file will contain the following:

- `pin_map_methods`: A list of methods used to register the pin map for the measurement plug-ins. Update `pin_map_path` variable with the pin map file path.
  - These line(s) of code can be removed in the non-pin-centric workflow.
- A loop that registers the PinMap for each Measurement Plug-in.

**Note:** Users must update the `sequence.py` file to define their sequences using the generated measurement plug-in clients.

### Step 4: Set Up Logging

- A basic logger package (`ni_sequence_logger`) is provided to log the execution results of the sequence.
- Install this logging package using the command,

 ```bash
 pip install <path_to_ni_sequence_logger-x.x.x-py3-none-any.whl>
 ```

- Once installed, the logging package will initialize the logging configuration for the script, helping capture logs from various operations throughout the sequence.

### Step 5: Execute the Sequence

- Run the `sequence.py` file to execute the sequence.
- The log will be saved as a CSV file in the current working directory.

```text
Note: Before creating clients, the tool automatically handles directory cleanup by,

- Clearing the content of the `__init__.py` file (if it exists).
- Removing all generated clients.
- Deleting the `sequence.py` file (if present).
```

## Note

- No dependency management: The user must take care of managing the dependencies for the respective sequence directory.
  - The sequencer doesn't generate a `pyproject.toml` file. Instead, the user must ensure that the necessary [dependencies](#dependencies) are installed.
