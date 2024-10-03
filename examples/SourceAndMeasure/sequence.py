from clients import nidcpowersourcedcvoltageclient, nidmmmeasurementclient
from sequence_logger import init_log

init_log()

pin_map_methods = [
    nidcpowersourcedcvoltageclient.register_pin_map,
    nidmmmeasurementclient.register_pin_map,
]

pin_map_path = r"examples\SourceAndMeasure\PinMap.pinmap"  # update your pinmap path here

# pinmap will be registered to all the instruments
for register_pin_map in pin_map_methods:
    register_pin_map(pin_map_path)

# write your sequence here
dcpower_result = nidcpowersourcedcvoltageclient.measure(pin_names=['DUTPin2'])
if(dcpower_result.in_compliance):
    nidmmmeasurementclient.measure(pin_name="DUTPin1")