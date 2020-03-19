import json
import requests
import hashlib


def get_article_url(path):
    URL_API = "https://en.wikipedia.org/w/api.php"
    params = {
        'format': 'json',
        'action': 'opensearch'
    }

    with open(path, encoding='utf8') as file:
        countries = json.load(file)
        for i, country in enumerate(countries):
            country_name = countries[i]['name']['common']
            params['search'] = country_name
            response = requests.get(URL_API, params)
            url = response.json()[3][0]
            yield {country_name: url}


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
    for country_url in get_article_url('countries.json'):
        countries_dict.update(country_url)
    with open('wiki_urls.json', 'w') as file:
        json.dump(countries_dict, file, indent=2)

    for md5_hash in get_md5('wiki_urls.json'):
        print(md5_hash)
