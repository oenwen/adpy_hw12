import json
import requests
import sys
import hashlib

class WikiCountries:

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, encoding='utf8')
        self.countries = json.load(self.file)
        self.i = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        URL_API = "https://en.wikipedia.org/w/api.php"
        params = {
            'format': 'json',
            'action': 'opensearch'
        }

        try:
            country_name = self.countries[self.i]['name']['common']
        except IndexError:
            raise StopIteration

        params['search'] = country_name
        response = requests.get(URL_API, params)
        url = response.json()[3][0]
        print(self.i)
        return {country_name: url}


def get_md5(path1):
    m = hashlib.md5()

    with open(path1) as file:
        file_json = json.load(file)
        for key in file_json:
            line = key + file_json[key]
            m.update(line.encode())
            yield m.hexdigest()


if __name__ == '__main__':

    countries_dict = {}
    for country in WikiCountries('countries.json'):
        countries_dict.update(country)
    with open('wiki_urls.json', 'w') as file:
        json.dump(countries_dict, file, indent=2)

    for md5_hash in get_md5('wiki_urls.json'):
        print(md5_hash)
