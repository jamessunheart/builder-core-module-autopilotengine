import time
from typing import Callable

class AutopilotEngine:
    def __init__(self, dashboard, evaluator, guardian, interval: int = 3600):
        self.dashboard = dashboard
        self.evaluator = evaluator
        self.guardian = guardian
        self.interval = interval
        self.paused = False

    def toggle_pause(self):
        self.paused = not self.paused

    def run_cycle(self):
        if self.paused:
            return "Paused. No actions taken."
        for module in self.dashboard.get_flagged_modules():
            try:
                self.dashboard.trigger_evaluation(module, self.evaluator)
            except Exception as e:
                self.guardian.handle_error(module, "trigger_evaluation", str(e))
        return "Cycle complete."

    def run_continuously(self):
        while True:
            print(self.run_cycle())
            time.sleep(self.interval)