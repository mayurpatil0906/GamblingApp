class StakeMonitor:

    def __init__(self):
        self.history = []
        self.peak = 0
        self.lowest = float("inf")

    def update(self, stake):
        self.history.append(stake)

        if stake > self.peak:
            self.peak = stake

        if stake < self.lowest:
            self.lowest = stake

    def get_stats(self):
        return {
            "peak": self.peak,
            "lowest": self.lowest,
            "changes": len(self.history)
        }