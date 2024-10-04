# Client Manager and Sequencer Tool

## Example: Source and Measure

This is a Python sequencer example that sequences two clients. `NI-DCPower` for sourcing and `NI-DMM` for measurement.

## What does this example accomplish?

- Generated client for `NI-DCPower` and `NI-DMM` measurement-plugins
- Registers the pinmap for the instruments using the start-up code provided.
- Call `measure` APIs from the measurement-plugin clients
- Sources with `NI-DCPower` first
  - If the result is in compliance,
    - Measures with `NI-DMM` second
- Logs the results and values

## How to run the example?

- Use the `.venv` created by the `src\python_sequencer\pyproject.toml` file.
  - Manually verify that all dependencies are installed correctly by reviewing the `sequence.py` file.
- Execute the `sequence.py` file directly.
- After execution, the results will be logged in `logs\` directory.
