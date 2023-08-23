import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_single_page(url):
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
            price_sqm = listing.find('div',
                                     class_='realty-preview-price realty-preview-price--sqm').text.replace(
                u'\xa0', '')
            title = listing.find('h3', class_='realty-preview-title').text.replace(u'\xa0', ' ')

            rooms = info_elements[0].text
            area = info_elements[1].text
            floor = info_elements[2].text
            building_type = info_elements[3].text
            materials = info_elements[4].text
            year = info_elements[5].text

            new_record = {'price_main': [price_main], 'price_sqm': [price_sqm], 'title': [title], 'rooms': [rooms],
                          'area': [area], 'floor': [floor], 'building_type': [building_type], 'materials': [materials],
                          'year': [year]}

            df = pd.concat([df, pd.DataFrame(new_record)], ignore_index=True)

    return df


class DataCollector:
    def __init__(self, url):
        self.url = url

    def parse_request(self):
        # df = pd.DataFrame()
        df = parse_single_page(self.url)

        self.url = self.url.replace('false', 'false&page='+ str(2))

        df = pd.concat([df, parse_single_page(self.url)], ignore_index=True)
        print(df)
        for i in range(3, 100):
            self.url = self.url.replace('page='+str(i-1), 'page=' + str(i))
            new_df = parse_single_page(self.url)
            if len(new_df) > 1:
                if (new_df.loc[0] == df.loc[0]).all() and (new_df.loc[1] == df.loc[1]).all():
                    break
            df = pd.concat([df, parse_single_page(self.url)], ignore_index=True)
            print(f'parsing {i} page')
            print(parse_single_page(self.url))

        print(df)


def main():
    # Оскільки пошук обмежено видачею 99 сторінок та ~ 2400 оголошеннями, то треба розбити пошук на декілька запитів
    # В нашому випадку підійде розбити видачу на 10 районів. url_1 - адреса першої сторінки видачі. Наступні
    # відрізняються останньою цифрою - від id=28748 до id=28757

    # наша перша сторінка пошуку: url = "https://market.lun.ua/uk/search?currency=UAH&geo_id=1&is_without_fee=false
    # &price_sqm_currency=UAH&section_id=1&sort=relevance&sub_geo_id=28748" ми розіб'єм цю адресу на 2 частини,
    # де остання частина буде числом "28748" - щоб можна було змінювати її лічильником.

    first_url = "https://market.lun.ua/uk/search?currency=UAH&geo_id=1&is_without_fee=false&price_sqm_currency=UAH" \
               "&section_id=1&sort=relevance&sub_geo_id=28748"

    test_url = "https://market.lun.ua/uk/search?currency=UAH&geo_id=1&is_without_fee=false&price_sqm_currency=UAH" \
               "&section_id=1&sort=relevance&sub_geo_id=28750"

    a = DataCollector(test_url)

    a.parse_request()

    # parse_single_page(test_url)
    pass


if __name__ == '__main__':
    main()
