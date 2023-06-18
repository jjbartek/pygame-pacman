import time

from enums.units import Units


class TimeUtils:
    @staticmethod
    def elapsed(past_time, unit=Units.Milliseconds):
        if unit == Units.Milliseconds:
            return time.time() * 1000 - past_time * 1000
        else:
            return time.time() - past_time
