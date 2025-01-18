import requests

import data_client2
from bs4 import BeautifulSoup


class Parser:
    links_to_pars = [
        'https://www.kufar.by/l/mebel',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MiwicGl0IjoiMjg4ODYwNDEifQ%3D%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MywicGl0IjoiMjg4ODYwNDEifQ%3D%3D'

    ]
    data_client_imp = data_client2.Postgresclient()
    @staticmethod
    def get_mebel_items(link):
        response = requests.get(link)
        mebel_data = response.text
        mebel_items = []
        to_parser = BeautifulSoup(mebel_data, 'html.parser')
        for elem in to_parser.find_all('a', class_='styles_wrapper__5FoK7'):
            try:
                price, decription = elem.text.split('р.')
                mebel_items.append((
                    elem['href'],
                    int(price.replace(' ', '')),
                    decription
                ))
            except:
                print(f' Цена не была указана. {elem.text}')
        return mebel_items


    def save_to_postgres(self, mebel_items):
        self.data_client_imp.create_mebel_table()
        for item in mebel_items:
            self.data_client_imp.insert(item[0], item[1], item[2])

    @staticmethod
    def save_to_csv(mebel_items):
        pandas.DataFrame(mebel_items).to_csv('mebel.csv', index=False)

    def run(self):
        mebel_items = []
        for link in Parser.links_to_pars:
            mebel_items.extend(self.get_mebel_items(link))
        self.save_to_postgres(mebel_items)
        self.save_to_csv(mebel_items)

Parser().run()