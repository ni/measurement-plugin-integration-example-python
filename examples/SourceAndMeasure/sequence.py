from clients import nidc_power_source_dc_voltage_client, ni_dmm_measurement_client
from sequence_logger import init_log

init_log()

pin_map_methods = [
    nidc_power_source_dc_voltage_client.register_pin_map,
    ni_dmm_measurement_client.register_pin_map,
]

pin_map_path = r"examples\SourceAndMeasure\PinMap.pinmap"  # TODO: Update your pin map path here.

# Register the pin map with all the measurement plug-in clients
for register_pin_map in pin_map_methods:
    register_pin_map(pin_map_path)

# TODO: Write your sequence logic here.
dcpower_result = nidc_power_source_dc_voltage_client.measure(pin_names=['DUTPin2'])
if(dcpower_result.in_compliance):
    ni_dmm_measurement_client.measure(pin_name="DUTPin1")