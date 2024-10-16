"""Generated client API for the 'NI-DCPower Source DC Voltage (Py)' measurement plug-in."""

from __future__ import annotations

import logging
import pathlib
import threading
import typing

import grpc
from google.protobuf import any_pb2, descriptor_pool
from google.protobuf.type_pb2 import Field
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2 as v2_measurement_service_pb2,
    measurement_service_pb2_grpc as v2_measurement_service_pb2_grpc,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient
from ni_measurement_plugin_sdk_service.grpc.channelpool import GrpcChannelPool
from ni_measurement_plugin_sdk_service.measurement.client_support import (
    ParameterMetadata,
    create_file_descriptor,
    deserialize_parameters,
    serialize_parameters,
)
from ni_measurement_plugin_sdk_service.pin_map import PinMapClient
from ni_measurement_plugin_sdk_service.session_management import PinMapContext

_logger = logging.getLogger(__name__)

_V2_MEASUREMENT_SERVICE_INTERFACE = "ni.measurementlink.measurement.v2.MeasurementService"


class Outputs(typing.NamedTuple):
    """Outputs for the 'NI-DCPower Source DC Voltage (Py)' measurement plug-in."""

    measurement_sites: typing.Sequence[int]
    measurement_pin_names: typing.Sequence[str]
    voltage_measurements: typing.Sequence[float]
    current_measurements: typing.Sequence[float]
    in_compliance: typing.Sequence[bool]


class NIDCPowerSourceDCVoltageClient:
    """Client for the 'NI-DCPower Source DC Voltage (Py)' measurement plug-in."""

    def __init__(
        self,
        *,
        discovery_client: typing.Optional[DiscoveryClient] = None,
        pin_map_client: typing.Optional[PinMapClient] = None,
        grpc_channel: typing.Optional[grpc.Channel] = None,
        grpc_channel_pool: typing.Optional[GrpcChannelPool] = None,
    ):
        """Initialize the Measurement Plug-In Client.

        Args:
            discovery_client: An optional discovery client.

            pin_map_client: An optional pin map client.

            grpc_channel: An optional gRPC channel targeting a measurement service.

            grpc_channel_pool: An optional gRPC channel pool.
        """
        self._initialization_lock = threading.RLock()
        self._service_class = "ni.examples.NIDCPowerSourceDCVoltage_Python"
        self._version = "0.0.1"
        self._grpc_channel_pool = grpc_channel_pool
        self._discovery_client = discovery_client
        self._pin_map_client = pin_map_client
        self._stub: typing.Optional[v2_measurement_service_pb2_grpc.MeasurementServiceStub] = None
        self._measure_response: typing.Optional[
            grpc.CallIterator[v2_measurement_service_pb2.MeasureResponse]
        ] = None
        self._configuration_metadata = {
            1: ParameterMetadata(
                display_name="pin_names",
                type=Field.Kind.ValueType(9),
                repeated=True,
                default_value=["Pin1"],
                annotations={
                    "ni/ioresource.instrument_type": "niDCPower",
                    "ni/type_specialization": "ioresource",
                },
                message_type="",
                field_name="pin_names",
                enum_type=None,
            ),
            2: ParameterMetadata(
                display_name="voltage_level",
                type=Field.Kind.ValueType(1),
                repeated=False,
                default_value=6.0,
                annotations={},
                message_type="",
                field_name="voltage_level",
                enum_type=None,
            ),
            3: ParameterMetadata(
                display_name="voltage_level_range",
                type=Field.Kind.ValueType(1),
                repeated=False,
                default_value=6.0,
                annotations={},
                message_type="",
                field_name="voltage_level_range",
                enum_type=None,
            ),
            4: ParameterMetadata(
                display_name="current_limit",
                type=Field.Kind.ValueType(1),
                repeated=False,
                default_value=0.01,
                annotations={},
                message_type="",
                field_name="current_limit",
                enum_type=None,
            ),
            5: ParameterMetadata(
                display_name="current_limit_range",
                type=Field.Kind.ValueType(1),
                repeated=False,
                default_value=0.01,
                annotations={},
                message_type="",
                field_name="current_limit_range",
                enum_type=None,
            ),
            6: ParameterMetadata(
                display_name="source_delay",
                type=Field.Kind.ValueType(1),
                repeated=False,
                default_value=0.0,
                annotations={},
                message_type="",
                field_name="source_delay",
                enum_type=None,
            ),
        }
        self._output_metadata = {
            1: ParameterMetadata(
                display_name="measurement_sites",
                type=Field.Kind.ValueType(5),
                repeated=True,
                default_value=None,
                annotations={},
                message_type="",
                field_name="measurement_sites",
                enum_type=None,
            ),
            2: ParameterMetadata(
                display_name="measurement_pin_names",
                type=Field.Kind.ValueType(9),
                repeated=True,
                default_value=None,
                annotations={},
                message_type="",
                field_name="measurement_pin_names",
                enum_type=None,
            ),
            3: ParameterMetadata(
                display_name="voltage_measurements",
                type=Field.Kind.ValueType(1),
                repeated=True,
                default_value=None,
                annotations={},
                message_type="",
                field_name="voltage_measurements",
                enum_type=None,
            ),
            4: ParameterMetadata(
                display_name="current_measurements",
                type=Field.Kind.ValueType(1),
                repeated=True,
                default_value=None,
                annotations={},
                message_type="",
                field_name="current_measurements",
                enum_type=None,
            ),
            5: ParameterMetadata(
                display_name="in_compliance",
                type=Field.Kind.ValueType(8),
                repeated=True,
                default_value=None,
                annotations={},
                message_type="",
                field_name="in_compliance",
                enum_type=None,
            ),
        }
        if grpc_channel is not None:
            self._stub = v2_measurement_service_pb2_grpc.MeasurementServiceStub(grpc_channel)
        self._create_file_descriptor()
        self._pin_map_context: PinMapContext = PinMapContext(pin_map_id="", sites=[0])

    @property
    def pin_map_context(self) -> PinMapContext:
        """The pin map context for the measurement."""
        return self._pin_map_context

    @pin_map_context.setter
    def pin_map_context(self, val: PinMapContext) -> None:
        if not isinstance(val, PinMapContext):
            raise TypeError(
                f"Invalid type {type(val)}: The given value must be an instance of PinMapContext."
            )
        self._pin_map_context = val

    @property
    def sites(self) -> typing.Optional[typing.List[int]]:
        """The sites where the measurement must be executed."""
        return self._pin_map_context.sites

    @sites.setter
    def sites(self, val: typing.List[int]) -> None:
        if self._pin_map_context is None:
            raise AttributeError(
                "Cannot set sites because the pin map context is None. Please provide a pin map context or register a pin map before setting sites."
            )
        self._pin_map_context = self._pin_map_context._replace(sites=val)

    def _get_stub(self) -> v2_measurement_service_pb2_grpc.MeasurementServiceStub:
        if self._stub is None:
            with self._initialization_lock:
                if self._stub is None:
                    service_location = self._get_discovery_client().resolve_service(
                        provided_interface=_V2_MEASUREMENT_SERVICE_INTERFACE,
                        service_class=self._service_class,
                        version=self._version,
                    )
                    channel = self._get_grpc_channel_pool().get_channel(
                        service_location.insecure_address
                    )
                    self._stub = v2_measurement_service_pb2_grpc.MeasurementServiceStub(channel)
        return self._stub

    def _get_discovery_client(self) -> DiscoveryClient:
        if self._discovery_client is None:
            with self._initialization_lock:
                if self._discovery_client is None:
                    self._discovery_client = DiscoveryClient(
                        grpc_channel_pool=self._get_grpc_channel_pool(),
                    )
        return self._discovery_client

    def _get_grpc_channel_pool(self) -> GrpcChannelPool:
        if self._grpc_channel_pool is None:
            with self._initialization_lock:
                if self._grpc_channel_pool is None:
                    self._grpc_channel_pool = GrpcChannelPool()
        return self._grpc_channel_pool

    def _get_pin_map_client(self) -> PinMapClient:
        if self._pin_map_client is None:
            with self._initialization_lock:
                if self._pin_map_client is None:
                    self._pin_map_client = PinMapClient(
                        discovery_client=self._get_discovery_client(),
                        grpc_channel_pool=self._get_grpc_channel_pool(),
                    )
        return self._pin_map_client

    def _create_file_descriptor(self) -> None:
        create_file_descriptor(
            input_metadata=list(self._configuration_metadata.values()),
            output_metadata=list(self._output_metadata.values()),
            service_name=self._service_class,
            pool=descriptor_pool.Default(),
        )

    def _create_measure_request(
        self, parameter_values: typing.List[typing.Any]
    ) -> v2_measurement_service_pb2.MeasureRequest:
        serialized_configuration = any_pb2.Any(
            type_url="type.googleapis.com/ni.measurementlink.measurement.v2.MeasurementConfigurations",
            value=serialize_parameters(
                self._configuration_metadata,
                parameter_values,
                f"{self._service_class}.Configurations",
            ),
        )
        return v2_measurement_service_pb2.MeasureRequest(
            configuration_parameters=serialized_configuration,
            pin_map_context=self._pin_map_context._to_grpc(),
        )

    def _deserialize_response(
        self, response: v2_measurement_service_pb2.MeasureResponse
    ) -> Outputs:
        return Outputs._make(
            deserialize_parameters(
                self._output_metadata,
                response.outputs.value,
                f"{self._service_class}.Outputs",
            )
        )

    def measure(
        self,
        pin_names: typing.Iterable[str] = ["Pin1"],
        voltage_level: float = 6.0,
        voltage_level_range: float = 6.0,
        current_limit: float = 0.01,
        current_limit_range: float = 0.01,
        source_delay: float = 0.0,
    ) -> Outputs:
        """Perform a single measurement.

        Returns:
            Measurement outputs.
        """
        stream_measure_response = self.stream_measure(
            pin_names,
            voltage_level,
            voltage_level_range,
            current_limit,
            current_limit_range,
            source_delay,
        )
        for response in stream_measure_response:
            result = response
        return result

    def stream_measure(
        self,
        pin_names: typing.Iterable[str] = ["Pin1"],
        voltage_level: float = 6.0,
        voltage_level_range: float = 6.0,
        current_limit: float = 0.01,
        current_limit_range: float = 0.01,
        source_delay: float = 0.0,
    ) -> typing.Generator[Outputs, None, None]:
        """Perform a streaming measurement.

        Returns:
            Stream of measurement outputs.
        """
        parameter_values = [
            pin_names,
            voltage_level,
            voltage_level_range,
            current_limit,
            current_limit_range,
            source_delay,
        ]
        with self._initialization_lock:
            if self._measure_response is not None:
                raise RuntimeError(
                    "A measurement is currently in progress. To make concurrent measurement requests, please create a new client instance."
                )
            request = self._create_measure_request(parameter_values)
            self._measure_response = self._get_stub().Measure(request)

        try:
            for response in self._measure_response:
                yield self._deserialize_response(response)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                _logger.debug("The measurement is canceled.")
            raise
        finally:
            with self._initialization_lock:
                self._measure_response = None

    def cancel(self) -> bool:
        """Cancels the active measurement call."""
        with self._initialization_lock:
            if self._measure_response:
                return self._measure_response.cancel()
            else:
                return False

    def register_pin_map(self, pin_map_path: pathlib.Path) -> None:
        """Registers the pin map with the pin map service.

        Args:
            pin_map_path: Absolute path of the pin map file.
        """
        pin_map_id = self._get_pin_map_client().update_pin_map(pin_map_path)
        self._pin_map_context = self._pin_map_context._replace(pin_map_id=pin_map_id)
