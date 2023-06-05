from datetime import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FILE_NAME = 'status_summary_{}.csv'
TIME_FORMAT = r'%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = dict()
        self.total = 0

    def process_item(self, item, spider):
        status = item['status']
        if status not in self.statuses:
            self.statuses[status] = 0
        self.statuses[status] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        RESULTS_DIR = BASE_DIR / 'results'
        with open(
            RESULTS_DIR
            / FILE_NAME.format(dt.now().strftime(TIME_FORMAT)),
            mode='w',
            encoding='utf-8',
        ) as self.f:
            self.f.write('Статус,Количество\n')
            for key in self.statuses.keys():
                self.f.write(f'{key},{self.statuses[key]}\n')
            self.f.write(f'Total,{self.total}\n')
