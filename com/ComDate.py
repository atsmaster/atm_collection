import datetime as dt


class ComDate:
    @classmethod
    def get_interval_val(cls, interval_cd):
        interval_val = None
        if interval_cd == '1m':
            interval_val = dt.timedelta(minutes=1)
        elif interval_cd == '1d':
            interval_val = dt.timedelta(days=1)
        return interval_val


