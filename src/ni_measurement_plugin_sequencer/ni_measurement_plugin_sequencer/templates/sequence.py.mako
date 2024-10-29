from clients import ${', '.join(instance_names)}
from ni_sequence_logger import init_log

init_log()

pin_map_methods = [
% for instance_name in instance_names:
% for func in callables:
    ${instance_name}.${func},
% endfor
% endfor
]

pin_map_path = r"path\to\pinmap\file.pinmap"  # TODO: Update your pin map path here.

# Register the pin map with all the measurement plug-in clients
for register_pin_map in pin_map_methods:
    register_pin_map(pin_map_path)

# TODO: Write your sequence logic here.
