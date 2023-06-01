from itemadapter import ItemAdapter

class PepParsePipeline:
    statuses = dict()
    total = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item['status']
        if status not in self.statuses:
            self.statuses[status] = 0
        self.statuses[status] += 1
        self.total += 1
        return item
    
    def close_spider(self, spider):
        with open('results/status_summary_%(time)s.csv', mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for key in self.statuses.keys():
                f.write(f'{key},{self.statuses[key]}\n')
            f.write(f'Total,{self.total}\n')
