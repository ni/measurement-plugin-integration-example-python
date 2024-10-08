# Example: Source and Measure DC Voltage

This Python sequencer example sequences two measurements, where the `NI-DCPower` is used for sourcing and `NI-DMM` for measurement.

## What does this example accomplish?

- Uses the clients generated for the NI-DCPower Source DC Voltage and NI-DMM measurement plug-ins.
- Registers the pin map using the provided start-up code.
- Calls the measure APIs from the respective measurement plug-in clients.
- Initiates sourcing with NI-DCPower.
  - If the result meets compliance standards:
    - Proceeds with measurement using NI-DMM.
- Logs the measured values and corresponding results.

## How to run the example?

- Ensure that you have the `ni-measurement-plugin-sdk-service` installed in your machine or virtual environment.
- Execute the `sequence.py` file directly.
- After execution, the results will be logged in `logs\` directory, which will get created in the current working directory.
