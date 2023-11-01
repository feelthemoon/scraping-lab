import csv
import requests
from bs4 import BeautifulSoup


def get_bs4_obj_from_html(url):
    html, bsObj = None, None

    try:
        html = requests.get(url)
    except requests.HTTPError:
        return None
    try:
        bsObj = BeautifulSoup(html.content, 'html.parser')
    except AttributeError as e:
        return None
    return bsObj


def parse_all_articles(bsObj: BeautifulSoup):
    articles_map = {}

    articles = bsObj.findAll('article')
    titles = bsObj.select('article h2')
    links = bsObj.select('h2 > a')
    authors = bsObj.select('.tm-user-info__username')
    date = bsObj.select('time')

    if len(articles) > 0:
        for i in range(len(articles)):
            articles_map[titles[i].get_text()] = {
                'link': 'https://habr.com/' + links[i].get('href'),
                'author': authors[i].get_text().replace(' ', '').replace('\n', ''),
                'date': date[i].get_text()
            }
        return articles_map

    return None

def write_to_csv(data: dict, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        for title in data.keys():
            writer.writerow(title + '\n' + 'Ссылка - ' +
                            data[title]['link'] + ', автор - ' +
                            data[title]['author'] + ', дата публикации - ' +
                            data[title]['date']
                            )
            writer.writerow('\n')


bsObj = get_bs4_obj_from_html("https://habr.com/ru/search/?q=NFT&target_type=posts&order=relevance")
write_to_csv(parse_all_articles(bsObj), './result.csv')
