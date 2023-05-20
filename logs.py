from datetime import datetime
import pandas as pd

class Log:
    def __init__(self, link):
        self.link = link
        self.time = datetime.now()


class LogsLibrary:
    def __init__(self):
        self.logs = []

    def add_click(self, link):
        self.logs.append(Log(link))

    def get_clicks_as_pandas(self):
        if len(self.logs) == 0:
            return pd.DataFrame(columns=['time', 'shortened_link'])
        return pd.DataFrame([{
            'time': log.time,
            'shortened_link': log.link.shortened_link
        } for log in self.logs])

    def get_total_clicks_as_pandas(self):
        if len(self.logs) == 0:
            return pd.DataFrame(columns=['shortened_link', 'total_clicks'])
        return self.get_clicks_as_pandas().groupby('shortened_link').count().rename(
            columns={'time': 'total_clicks'}
        )

    def get_logs_by_shorten_link(self, shorten_link):
        return [log for log in self.logs if log.link.shorten_link == shorten_link]
