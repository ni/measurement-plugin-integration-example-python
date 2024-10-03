from clients import ${', '.join(instance_names)}
from sequence_logger import init_log

init_log()

pin_map_methods = [
% for instance_name in instance_names:
% for func in callables:
    ${instance_name}.${func},
% endfor
% endfor
]

pin_map_path = r"path\\to\\pinmap\\file"  # update your pinmap path here

# pinmap will be registered to all the instruments
for register_pin_map in pin_map_methods:
    register_pin_map(pin_map_path)

# write your sequence here
