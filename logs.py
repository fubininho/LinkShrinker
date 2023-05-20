import datatime
import pandas as pd

class Log:
    def __init__(self, link):
        self.link = link
        self.time = datetime.datetime.now()


class LogsLibrary:
    def __init__(self):
        self.logs = []

    def add_click(self, link):
        self.logs.append(Log(link))

    def get_clicks_as_pandas(self):
        return pd.DataFrame([{
            'time': log.time,
            'shorten_link': log.link.shorten_link
        } for log in self.logs])

    def get_total_clicks_as_pandas(self):
        return self.get_clicks_as_pandas().groupby('shorten_link').count().rename(
            columns={'time': 'total_clicks'}
        )

    def get_logs_by_shorten_link(self, shorten_link):
        return [log for log in self.logs if log.link.shorten_link == shorten_link]
