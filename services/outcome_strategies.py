import random


class RandomOutcomeStrategy:
    def determine_outcome(self, win_probability):
        return "WIN" if random.random() <= float(win_probability) else "LOSS"


class WeightedProbabilityStrategy:
    def determine_outcome(self, win_probability, house_edge=0.05):
        adjusted_probability = max(0.0, min(1.0, float(win_probability) - float(house_edge)))
        return "WIN" if random.random() <= adjusted_probability else "LOSS"