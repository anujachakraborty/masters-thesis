from feral3gp import feral

from exercise_3.settings import SimulationSettings
from exercise_3.vehicle_control.messaging import Message


class VehicleController(feral.EventTriggeredWorker):
    def __init__(self, name: str, simulation_settings: SimulationSettings):
        super().__init__(name)
        self.simulation_settings = simulation_settings

    def message_received(self, event, rx_port):
        distance_m = event.getValue()

        if distance_m <= self.get_braking_distance_m():
            self.out_port.send(feral.event(Message.EMERGENCY_BRAKE.value))

    def get_braking_distance_m(self):
        braking_distance_m = ((self.simulation_settings.speed_m_per_s * 3.6 / 10) ** 2)
        braking_distance_m = max(braking_distance_m + 1, braking_distance_m * 1.05)
        return braking_distance_m
