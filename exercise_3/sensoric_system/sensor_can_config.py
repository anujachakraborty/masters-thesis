from feral3gp import feral

from feral3gp.feral import CANNodeConfig, MessageTypeConfig, MessageType, CANConfig

distance_evaluator_node = CANNodeConfig(
    name="distance_evaluator_node",
    drop_duplicated_frames=True,
    message_types=[
        MessageTypeConfig(
            type=MessageType.TX,
            address="fd:2",
            simulated_payload_size=4,
            port_name="distance_evaluator_tx"
        ),
        MessageTypeConfig(
            type=MessageType.RX,
            address="fd:3",
            simulated_payload_size=4,
            port_name="distance_evaluator_rx"
        )
    ]
)

gateway_node = CANNodeConfig(
    name="gateway_node",
    drop_duplicated_frames=True,
    message_types=[
        MessageTypeConfig(
            type=MessageType.RX,
            address="fd:2",
            simulated_payload_size=4,
            port_name="gateway_rx"
        )]
)

sensor_main_node = CANNodeConfig(
    name="sensor_main_node",
    drop_duplicated_frames=True,
    message_types=[
        MessageTypeConfig(
            type=MessageType.TX,
            address="fd:3",
            simulated_payload_size=4,
            port_name="sensor_main_tx"
        )]
)

sensor_redundancy_node = CANNodeConfig(
    name="sensor_redundancy_node",
    drop_duplicated_frames=True,
    message_types=[
        MessageTypeConfig(
            type=MessageType.TX,
            address="fd:3",
            simulated_payload_size=4,
            port_name="sensor_redundancy_tx"
        )],
    fault_injectors=[
        feral.FaultInjectorConfig(
            error_model=feral.ErrorModelType.SENDER_LINK_FAILURE,
            #error_processor=feral.ErrorProcessorType.DROP_FRAME,
            error_processor=feral.ErrorProcessorType.CHANGE_SIGN_DOUBLE,
            start_time=feral.millis(11000),
            end_time=feral.millis(12000)
        )]  
)

config = CANConfig(
    name="Sensors CAN Bus",
    bit_rate=100_000,
    bit_stuffing_mode=feral.BitStuffingMode.NONE,
    log_transmissions=False,
    nodes=[distance_evaluator_node, gateway_node, sensor_main_node, sensor_redundancy_node]
)
