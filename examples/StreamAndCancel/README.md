# Stream and Cancel measurement

This Python sequencer example demonstrates how to stream a measurement and cancel the streaming measurement at a certain condition.

## What does this example accomplish?

- Uses the client generated for the **Conway's Game of Life** measurement plug-in.
- Calls the `stream_measure` API from the generated client.
- Iterate through the generator for output, as this is a streaming measurement plug-in.
  - If the generation is equal to 10
    - Cancels the measurement.
- Handles the cancel exception.
- Logs the measured values and corresponding results.

## How to run the example?

- Ensure that you have the `ni-measurement-plugin-sdk-service` installed in your machine or virtual environment.
- Execute the `sequence.py` file directly.
- After execution, the results will be logged in the `logs\` directory, which will get created in the current working directory.
