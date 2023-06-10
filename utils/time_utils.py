import time


class TimeUtils:
    @staticmethod
    def time_elapsed_since(past_time):
        return time.time() * 1000 - past_time * 1000
