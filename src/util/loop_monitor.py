import time

class LoopMonitor:
    def __init__(self):
        self.frequency = None
        self.last_tick = None

    def tick(self):
        current_time = time.time()

        if self.last_tick is None:
            self.frequency = 0
            self.last_tick = current_time
            return

        self.frequency = 1.0 / (current_time - self.last_tick)
        self.last_tick = current_time
