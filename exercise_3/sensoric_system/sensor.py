from feral3gp import feral

from exercise_3.settings import SimulationSettings


class FrontDistanceSensor(feral.TimeTriggeredWorker):
    def __init__(self, name: str, simulation_setting: SimulationSettings):
        super().__init__(name)
        self.simulation_setting = simulation_setting

    def time_step(self):
        distance_to_obstacle = get_obstacle_distance(self.simulation_setting, self.get_simulation_time())
        distance_to_obstacle += (self.simulation_setting.random.nextDouble(-1,1)*0.1)
        self.out_port.send(feral.event(distance_to_obstacle))


def get_obstacle_distance(simulation_setting: SimulationSettings, simulation_time_ns: float) -> float:
    simulation_time_s = simulation_time_ns / 1_000_000_000
    distance_traveled = simulation_setting.speed_m_per_s * simulation_time_s

    return simulation_setting.starting_distance_m - distance_traveled
