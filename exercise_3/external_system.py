from feral3gp import feral as feral
from feral3gp.feral.fcapi.client import FCAPIClient
from feral3gp.feral.fcapi.sync_cb_listener import SyncCBListener
from feral3gp.feral import nanos, seconds


class ExternalSender:

    def __init__(self):
        self.client = FCAPIClient(feral.TransmissionBackend.TCP)
        self.handle = self.client.connect("localhost", 51899, "localhost", "External")

    def start_transmission(self):
        sync_end_time = seconds(7)

        self.client.sync(self.handle, seconds(1))
        self.client.sync(self.handle, seconds(2))
        self.client.sync(self.handle, seconds(3))
        self.client.sync(self.handle, seconds(4))
        self.client.sync(self.handle, seconds(5))
        self.client.sync(self.handle, seconds(6))
        self.client.sync(self.handle, seconds(7))

        self.client.start_sim(self.handle)
        self.client.wait(self.handle)

        while True:
            current_time = self.client.get_sim_time(self.handle)
            self.client.tx(self.handle, [42])

            self.client.continue_(self.handle)

            if current_time >= sync_end_time:
                break

            self.client.wait(self.handle)

        self.client.disconnect_all()


if __name__ == '__main__':
    sender = ExternalSender()
    sender.start_transmission()
