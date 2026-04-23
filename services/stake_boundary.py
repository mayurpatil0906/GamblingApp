class StakeBoundary:

    def __init__(self, min_limit, max_limit):
        self.min_limit = min_limit
        self.max_limit = max_limit

    def validate(self, stake):
        if stake < self.min_limit:
            return False, "Below minimum limit"
        if stake > self.max_limit:
            return False, "Above maximum limit"
        return True, "Within limits"