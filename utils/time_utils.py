import time


class TimeUtils:
    @staticmethod
    def time_elapsed(past_time):
        return time.time() * 1000 - past_time * 1000
