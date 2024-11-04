# Sequence Logger

A Python package that logs instance method calls, parameters, and return values in CSV format. Useful for debugging and tracing execution flows in systems with multiple interacting classes.

## Installation

```bash
pip install <path_to_ni_sequence_logger-x.x.x-py3-none-any.whl>
```

## Usage

```python
from ni_sequence_logger import init_log

# Initialize logging
init_log()

# Now instance method calls will be automatically logged
```

## Example Output

```csv
2024-10-03 11:18:54,INFO,Method Call: NIDCPowerSourceDCVoltageClient.register_pin_map
2024-10-03 11:18:54,INFO,Arguments: (pin_map_path='C:\\Path\\To\\PinMap.pinmap')
2024-10-03 11:18:54,INFO,Return: None
```

## Features

- Logs method name, parameters, and return values
- Captures exceptions with traceback
- Organizes logs by date in CSV format
- Only logs instance methods (not static or module-level functions)

## Configuration

By default, logs methods from modules starting with 'clients.'. Modify `apply_logging_to_all_modules` function to change this behavior.

Logs are stored in CSV files in a 'logs' directory within your current working directory.
