from typing import List

from feral3gp import feral


class DistanceEvaluator(feral.EventTriggeredWorker):
    def __init__(self, name: str):
        super().__init__(name)
        self.distance_values: List[float] = []
        self.last_valid_distance: float = -1

    def message_received(self, event, rx_port):
        received_distance = event.getValue()
        self.distance_values.append(received_distance)

        distance = self.get_latest_valid_distance()
        if distance > -1:
            self.schedule_delta_timer(feral.millis(10), 0)
        else:
            self.get_console().warning(f"No valid Distance available")

    def timer_expired(self, timed_event):
        self.out_port.send(feral.event(self.get_latest_valid_distance()))

    def get_latest_valid_distance(self) -> float:
        if len(self.distance_values) < 2:
            return -1

        distance = self.distance_values[-1]
        distance_check = self.distance_values[-2]

        tolerance = 0.2
        if abs(distance - distance_check)<tolerance:
        #if distance == distance_check:
            self.last_valid_distance = distance
            return distance
        else:
            return self.last_valid_distance
