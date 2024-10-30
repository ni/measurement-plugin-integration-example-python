# An Example Measurement Plug-In Sequencer for Python

## Overview

This tool serves as a reference for integrating the Measurement Plug-In Client Generator to generate measurement plug-in clients and showcase the sequencing of measurement plug-ins using the generated clients.

<!-- The Note here doesn't sound right and should be updated. -->
***Note:** Please read [Client Integration](/ClientIntegration.md) before proceeding.*

## Workflow Diagram

![sequencer-example-workflow-diagram](./docs/images/sequencer-example-workflow-diagram.png)

## Dependencies
- Python 3.9 or later
<!-- On further thought, this content reads redundant. -->
- The Measurement Plug-In Sequencer depends on:
  - ni-measurement-plugin-sdk-service
  - ni-measurement-plugin-sdk-generator
- To execute the generated sequence, the following dependency is required:
  - ni-sequence-logger

Please download the `ni_sequence_logger-x.x.x-py3-none-any.whl` file from the latest release assets.

## Steps to use the Sequencer tool

### Step 1: Install the Package

After downloading the `ni_measurement_plugin_sequencer-x.x.x-py3-none-any.whl` wheel file, install the package using the command below.

```bash
pip install /path/to/ni_measurement_plugin_sequencer-x.x.x-py3-none-any.whl
```

### Step 2: Run the Sequencer

To run the `ni-measurement-plugin-sequencer`, open your command line and enter:

```bash
ni-measurement-plugin-sequencer /path/to/sequence/directory
```

- **/path/to/sequence/directory**: Specify the directory path where the generated clients and sequence files will be stored. Confirm that the directory exists and has the necessary write permissions.

### Step 3: Review the Generated Sequence File

The generated `sequence.py` file will contain the following:
<!-- Instruction for non-pin centric workflow is missing and the following instructions should be rephrased -->
- `pin_map_methods`: A list of methods used to register the pin map for the measurement plug-ins. Update `pin_map_path` variable with the pin map file path. 
- A loop that registers the PinMap for each Measurement Plug-in.

**Note:** Users must update this file <!--(which file?)--> to define their own sequences using the generated clients.

### Step 5: Set Up Logging

- A basic logger package (`ni-sequence-logger`) is provided to log the execution results of the sequence.
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

### Example Usage - This section looks redundant - Could be removed

```bash
ni-measurement-plugin-sequencer /my/sequence/directory
```

This command generates new clients and a sequence file in the `/my/sequence/directory` directory.

## Note

- No dependency management: The user must take care of managing the dependencies for the respective sequence directory.
  - The sequencer doesn't generate a `pyproject.toml` file. Instead, the user must ensure that the necessary [dependencies](#dependencies) are installed.
