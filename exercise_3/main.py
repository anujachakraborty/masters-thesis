import sys
import logging
from feral3gp import feral

from exercise_3.sensoric_system import sensor_can_config
from exercise_3.sensoric_system.distance_evaluator import DistanceEvaluator
from exercise_3.sensoric_system.sensor import FrontDistanceSensor
from exercise_3.settings import SimulationSettings
from exercise_3.vehicle_control import vehicle_control_can_config
from exercise_3.vehicle_control.brake import Brake
from exercise_3.vehicle_control.gateway import Gateway
from exercise_3.vehicle_control.vehicle_controller import VehicleController

logging.basicConfig(level=logging.INFO)


def run_simulation(simulation_setting: SimulationSettings):
    # Set up the ECUs

    # Sensoric System
    front_distance_sensor = FrontDistanceSensor("Front Distance Sensor", simulation_setting)
    front_distance_sensor_redundancy = FrontDistanceSensor("Front Distance Sensor Redundancy", simulation_setting)
    distance_evaluator = DistanceEvaluator("Distance Evaluator")

    sensors_can = feral.can(sensor_can_config.config)

    # Vehicle Control System
    gateway = Gateway("Gateway")
    vehicle_controller = VehicleController("Vehicle Controller", simulation_setting)
    brake = Brake("Brake")

    vehicle_control_can = feral.can(vehicle_control_can_config.config)

    # Set Up Connection
    feral.link(front_distance_sensor, "output", sensors_can, "sensor_main_tx")
    feral.link(front_distance_sensor_redundancy, "output", sensors_can, "sensor_redundancy_tx")
    feral.link(sensors_can, "distance_evaluator_rx", distance_evaluator, "input")

    feral.link(distance_evaluator, "output", sensors_can, "distance_evaluator_tx")
    feral.link(sensors_can, "gateway_rx", gateway, "input")

    feral.link(gateway, "output", vehicle_control_can, "gateway_tx")

    feral.link(vehicle_control_can, "vehicle_controller_rx", vehicle_controller, "input")
    feral.link(vehicle_controller, "output", vehicle_control_can, "vehicle_controller_tx")
    feral.link(vehicle_control_can, "brake_rx", brake, "input")

    feral.set_step_size(simulation_setting.sensor_time_step_ns)
    feral.start(simulation_setting.get_simulation_duration_ns())
    logging.info(f"Minimum Braking Distance: {simulation_setting.get_minimum_braking_distance()}")
    if brake.time_of_break_signal_ns == 0 or brake.time_of_break_signal_ns > simulation_setting.get_last_ns_for_brake_signal():
        logging.error(f"Brake signal arrived at {brake.time_of_break_signal_ns / 1_000_000_000}s")
        logging.error(
            f"Brake Signal arrived too late -- Latest Possible: {simulation_setting.get_last_ns_for_brake_signal() / 1_000_000_000}s ")
        sys.exit(1)

    logging.info(
        f"Brake Signal arrived on time -- Latest Possible: {simulation_setting.get_last_ns_for_brake_signal() / 1_000_000_000}s ")


if __name__ == "__main__":
    settings = SimulationSettings(speed_m_per_s=15, starting_distance_m=200,
                                  sensor_time_step_ns=feral.millis(10))
    run_simulation(settings)
