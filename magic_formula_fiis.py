import csv
from collections import defaultdict
from typing import List


class FII:
    def __init__(self, ticker: str, dy: str, pvp: str, liquidez: str):
        self.ticker = ticker
        self.dy = self.parse_float(dy)
        self.pvp = self.parse_float(pvp)
        self.liquidez = self.parse_float(liquidez)

    def parse_float(self, value: str) -> float:
        if value:
            return float(value.replace('.', '').replace(',', '.'))

class MagicFormula:
    def __init__(self):
        self.fiis_rank = defaultdict(int)

    def run(self, fiis: List[FII]):
        fiis = self.filter_positive_pvp(fiis)
        fiis = self.filter_positive_dy(fiis)
        fiis = self.filter_liquidez(fiis)
        fiis_by_dy = self.order_by_dy(fiis)
        fiis_by_pvp = self.order_by_pvp(fiis)
        self.add_to_rank(fiis_by_dy)
        self.add_to_rank(fiis_by_pvp)
        best_fiis = self.get_best_fiis()
        self.print_and_write_file(best_fiis)

    def filter_positive_pvp(self, fiis_list):
        return [fii for fii in fiis_list if fii.pvp and fii.pvp > 0]

    def filter_positive_dy(self, fiis_list):
        return [fii for fii in fiis_list if fii.dy and fii.dy > 0]

    def filter_liquidez(self, fiis_list):
        return [fii for fii in fiis_list if fii.liquidez and fii.liquidez > 200000]

    def order_by_dy(self, fiis_list):
        return [fii.ticker for fii in sorted(fiis_list, key=lambda fii: -fii.pl)]
    
    def order_by_pvp(self, fiis_list):
        return [fii.ticker for fii in sorted(fiis_list, key=lambda fii: fii.pvp)]

    def add_to_rank(self, fiis_list):
        for idx, ticker in enumerate(fiis_list):
            self.fiis_rank[ticker] += idx

    def get_best_fiis(self):
        return sorted(self.fiis_rank.items(), key=lambda par: par[1])[:15]

    def print_and_write_file(self, fiis_list):
        print(fiis_list)
        with open('resultado-fiis.txt', 'w') as f:
            for ticker, value in fiis_list:
                f.write(ticker + '\n')


f = open('fiis-list.csv')

reader = csv.DictReader(f, delimiter=';')
fiis = [
    FII(
        row['TICKER'], row['DY'], row['P/VP'],
        row[' LIQUIDEZ MEDIA DIARIA']
    )
    for row in reader
]

MagicFormula().run(fiis)
