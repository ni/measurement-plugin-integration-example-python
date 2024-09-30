# Client Manager and Sequencer Tool

## Example: Source and Measure

This is a Python sequencer example that sequences two clients. `NI-DCPOWER` for sourcing and `NI-DMM` for measurement.

## What does this example accomplish?

- Generated client for `NI-DCPOWER` and `NI-DMM` measurement-plugins
- Registers the pinmap for the instruments using the start-up code provided.
- Call `measure` APIs from the measurement-plugin clients
- Sources with `NI-DCPOWER` first
  - If the result is in compliance,
    - Measures with `NI-DMM` second
- Logs the results and values
