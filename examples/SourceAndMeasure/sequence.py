from clients import nidc_power_source_dc_voltage_client, ni_dmm_measurement_client
from sequence_logger.sequence_logger import init_log

init_log()

pin_map_methods = [
    nidc_power_source_dc_voltage_client.register_pin_map,
    ni_dmm_measurement_client.register_pin_map,
]

pin_map_path = r"examples\SourceAndMeasure\PinMap.pinmap"  # update your pinmap path here

# pinmap will be registered to all the instruments
for register_pin_map in pin_map_methods:
    register_pin_map(pin_map_path)

# write your sequence here
dcpower_result = nidc_power_source_dc_voltage_client.measure(pin_names=['DUTPin2'])
if(dcpower_result.in_compliance):
    ni_dmm_measurement_client.measure(pin_name="DUTPin1")