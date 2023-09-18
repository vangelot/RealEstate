import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import os


def parse_single_page(url, district):
    """
    Дана функція може зчитати всі записи за даним ULR, записати результат в датафрейм та повернути його
    :return: - повертає датафрейм з записами
    """
    df = pd.DataFrame()
    response = requests.get(url)
    response.encoding = 'urf-8'

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('div', class_='realty-preview__content-column')
        for listing in listings:
            info_elements = listing.find_all('span', class_='realty-preview-info')

            if len(info_elements) < 8:
                continue

            price_main = listing.find('div',
                                      class_='realty-preview-price realty-preview-price--main').text.replace(
                u'\xa0', '')

            # ціну за м2 можна видалити бо це похідна від 2х існуючих критеріїв
            # price_sqm = listing.find('div',
            #                          class_='realty-preview-price realty-preview-price--sqm').text.replace(
            #     u'\xa0', '')
            title = listing.find('h3', class_='realty-preview-title').text.replace(u'\xa0', ' ')

            rooms = info_elements[0].text
            area = info_elements[1].text
            floor = info_elements[2].text
            building_type = info_elements[3].text
            materials = info_elements[4].text
            year = info_elements[5].text

            # запис без ціни за м2:
            new_record = {'price_main': [price_main], 'title': [title], 'rooms': [rooms],
                          'area': [area], 'floor': [floor], 'building_type': [building_type], 'materials': [materials],
                          'year': [year], 'district': [district]}

            # new_record = {'price_main': [price_main], 'price_sqm': [price_sqm], 'title': [title], 'rooms': [rooms],
            #               'area': [area], 'floor': [floor], 'building_type': [building_type], 'materials': [materials],
            #               'year': [year]}

            df = pd.concat([df, pd.DataFrame(new_record)], ignore_index=True)
    else:
        print("ERROR: PAGE Can't be read")

    return df


class DataCollector:
    def __init__(self, dict_of_districts, url):
        self.basic_url = url
        self.dict_of_districts = dict_of_districts

    def parse_district(self, district_name):
        """
        :return:
        """
        # df = pd.DataFrame()
        district_url = self.basic_url + self.dict_of_districts[district_name]

        # parsing 1st page:
        print(f'parsing 1 page, in district {district_name}')
        df = parse_single_page(district_url, district_name)
        len_df_first = len(df)

        # parsing 2nd page:
        district_url = district_url.replace('false', 'false&page=' + str(2))
        print(f'parsing 2 page, in district {district_name}')
        df = pd.concat([df, parse_single_page(district_url, district_name)], ignore_index=True)
        if len(df) == len_df_first:
            return df

        for i in range(3, 100):
            district_url = district_url.replace('page=' + str(i - 1), 'page=' + str(i))
            new_df = parse_single_page(district_url, district_name)
            if len(new_df) > 1:
                if (new_df.loc[0] == df.loc[0]).all() and (new_df.loc[1] == df.loc[1]).all():
                    break
            df = pd.concat([df, parse_single_page(district_url, district_name)], ignore_index=True)
            print(f'parsing {i} page, in district {district_name}')
            # print(parse_single_page(district_url))
        return df

    def parse_force(self):

        file_name = input("\nВи хочете почати примусовий парсинг в новий або існуючий файл\n"
              "введіть його ім'я: ")

        df = pd.DataFrame()
        # k = 0
        for key in self.dict_of_districts.keys():
            new_df = self.parse_district(key)

            df = pd.concat([df, new_df], ignore_index=True)

            # для тесту парсингу - парсити тільки перші 5 районів
            # k += 1
            # if k == 5:
            #     break

        df.to_csv(file_name + '.csv', index=False)

        return df


def main():

    """
    Задача: завантажити всі дані з сайту
    Етапи:
    1) зчитати Json файл з районами
    2) записати всі дані спочатку в змінну типу датафрейм, а потім - в кінцевий файл
    """

    with open('microDistricts.json', 'r', encoding='utf-8') as json_file:
        districts = json.load(json_file)

    # запам'ятовуємо базове посилання
    basic_url = districts['basic_url']

    # видаляємо зі словника перші два записи:
    districts.pop('comments'); districts.pop('basic_url', None)

    data_collector = DataCollector(districts, basic_url)

    print(data_collector.parse_force())

    # df2 = pd.read_csv('data.csv')
    # print(df2.iloc[0])


if __name__ == '__main__':
    main()
