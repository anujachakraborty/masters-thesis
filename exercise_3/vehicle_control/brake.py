from feral3gp import feral

from exercise_3.vehicle_control.messaging import Message


class Brake(feral.EventTriggeredWorker):
    def __init__(self, name: str):
        super().__init__(name)
        self.time_of_break_signal_ns: float = 0

    def message_received(self, event, rx_port):
        message = event.getValue()

        if self.time_of_break_signal_ns != 0:
            return

        if message == Message.EMERGENCY_BRAKE.value:
            self.time_of_break_signal_ns = self.get_simulation_time()
            self.get_console().info(f"Received Brake Signal at {self.get_simulation_time() / 1_000_000_000}s")
