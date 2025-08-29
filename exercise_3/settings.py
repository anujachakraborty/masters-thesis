from dataclasses import dataclass
from feral3gp import feral


@dataclass
class SimulationSettings:
    speed_m_per_s: float
    starting_distance_m: float
    sensor_time_step_ns: float
    random = feral.random(42)

    def get_simulation_duration_ns(self) -> float:
        duration_ms = (self.starting_distance_m / self.speed_m_per_s) * 1000
        return feral.millis(int(duration_ms))

    def get_minimum_braking_distance(self) -> float:
        braking_distance_m = (self.speed_m_per_s * 3.6 / 10) ** 2  # Bremsweg
        additional_braking_m = 1

        return braking_distance_m + additional_braking_m

    def get_last_ns_for_brake_signal(self) -> float:
        duration_s = self.get_simulation_duration_ns() / 1_000_000_000
        braking_distance_m = self.get_minimum_braking_distance()
        braking_duration_s = braking_distance_m / self.speed_m_per_s

        return (duration_s - braking_duration_s) * 1_000_000_000

    def get_speed_in_km_per_h(self):
        return self.speed_m_per_s * 3.6
