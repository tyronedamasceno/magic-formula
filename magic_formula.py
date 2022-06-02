import csv
from collections import defaultdict
from typing import List


class Acao:
    def __init__(self, ticker: str, ebit: str, pl: str, roe: str, liquidez: str):
        self.ticker = ticker
        self.ebit = self.parse_float(ebit)
        self.pl = self.parse_float(pl)
        self.roe = self.parse_float(roe)
        self.liquidez = self.parse_float(liquidez)

    def parse_float(self, value: str) -> float:
        if value:
            return float(value.replace('.', '').replace(',', '.'))

class MagicFormula:
    def __init__(self):
        self.acoes_rank = defaultdict(int)

    def run(self, acoes: List[Acao]):
        acoes = self.filter_positive_ebit(acoes)
        acoes = self.filter_pl_greater_than_5(acoes)
        acoes = self.filter_liquidez(acoes)
        acoes_by_pl = self.order_by_pl(acoes)
        acoes_by_roe = self.order_by_roe(acoes)
        self.add_to_rank(acoes_by_pl)
        self.add_to_rank(acoes_by_roe)
        best_acoes = self.get_best_acoes()
        keep_acoes = self.get_keep_acoes()
        self.print_and_write_file(best_acoes, keep_acoes)

    def filter_positive_ebit(self, acoes_list):
        return [acao for acao in acoes_list if acao.ebit and acao.ebit > 0]

    def filter_pl_greater_than_5(self, acoes_list):
        return [acao for acao in acoes_list if acao.pl and acao.pl > 5]

    def filter_liquidez(self, acoes_list):
        return [acao for acao in acoes_list if acao.liquidez and acao.liquidez > 150000]

    def order_by_pl(self, acoes_list):
        return [acao.ticker for acao in sorted(acoes_list, key=lambda acao: acao.pl)]
    
    def order_by_roe(self, acoes_list):
        return [acao.ticker for acao in sorted(acoes_list, key=lambda acao: -acao.roe)]

    def add_to_rank(self, acoes_list):
        for idx, ticker in enumerate(acoes_list):
            self.acoes_rank[ticker] += idx

    def get_best_acoes(self):
        return sorted(self.acoes_rank.items(), key=lambda par: par[1])[:20]

    def get_keep_acoes(self):
        return sorted(self.acoes_rank.items(), key=lambda par: par[1])[20:40]

    def print_and_write_file(self, acoes_list, keep_list):
        print(acoes_list)
        print('\n')
        print(keep_list)
        with open('resultado.txt', 'w') as f:
            for ticker, value in acoes_list:
                f.write(ticker + '\n')
            f.write('\nTo keep: \n')
            for ticker, value in keep_list:
                f.write(ticker + '\n')


f = open('acoes-list.csv')

reader = csv.DictReader(f, delimiter=';')
acoes = [
    Acao(
        row['TICKER'], row['MARGEM EBIT'], row['P/L'],
        row['ROE'], row[' LIQUIDEZ MEDIA DIARIA']
    )
    for row in reader
]

MagicFormula().run(acoes)
