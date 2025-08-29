from feral3gp import feral


class Gateway(feral.EventTriggeredWorker):
    def __init__(self, name: str):
        super().__init__(name)

    def message_received(self, event, rx_port):
        self.out_port.send(event)
