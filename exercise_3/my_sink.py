from feral3gp import feral


class MySink(feral.EventTriggeredWorker):
    def __init__(self, name):
        super().__init__(name)

        self.messages = []

    def message_received(self, event, rx_port):
        rx_value = event.getValue()
        array = []
        for value in rx_value:
            array.append(value)
        self.messages.append(
            {
                "time": self.get_simulation_time(),
                "value": array,
            }
        )

    def terminate(self):
        self.get_console().info(f"Messages Received: {len(self.messages)}")
