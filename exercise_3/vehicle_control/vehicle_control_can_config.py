from feral3gp import feral

from feral3gp.feral import CANNodeConfig, MessageTypeConfig, MessageType, CANConfig

vehicle_controller_node = CANNodeConfig(
    name="vehicle_controller_node",
    drop_duplicated_frames=False,
    message_types=[
        MessageTypeConfig(
            type=MessageType.TX,
            address="fd:4",
            simulated_payload_size=4,
            port_name="vehicle_controller_tx"
        ),
        MessageTypeConfig(
            type=MessageType.RX,
            address="fd:2",
            simulated_payload_size=4,
            port_name="vehicle_controller_rx"
        )
    ],
    fault_injectors=[
        feral.FaultInjectorConfig(
            error_model=feral.ErrorModelType.SENDER_LINK_FAILURE,
            error_processor=feral.ErrorProcessorType.DROP_FRAME,
            start_time=feral.millis(300),
            end_time=feral.millis(600)
        )]  
)

gateway_node = CANNodeConfig(
    name="gateway_node",
    drop_duplicated_frames=False,
    message_types=[
        MessageTypeConfig(
            type=MessageType.TX,
            address="fd:2",
            simulated_payload_size=4,
            port_name="gateway_tx"
        )]
)

brake_node = CANNodeConfig(
    name="brake_node",
    drop_duplicated_frames=False,
    message_types=[
        MessageTypeConfig(
            type=MessageType.RX,
            address="fd:4",
            simulated_payload_size=4,
            port_name="brake_rx"
        )]
)

config = CANConfig(
    bit_rate=100_000,
    bit_stuffing_mode=feral.BitStuffingMode.NONE,
    log_transmissions=False,
    nodes=[vehicle_controller_node, gateway_node, brake_node]
)
