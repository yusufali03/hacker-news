import requests
from bs4 import BeautifulSoup
import pprint


res = requests.get("https://news.ycombinator.com/")
res2 = requests.get("https://news.ycombinator.com/?p=2")

soup = BeautifulSoup(res.text, "html.parser")
soup2 = BeautifulSoup(res2.text, "html.parser")
links = soup.select(".titleline > a")
subtext = soup.select(".subtext")
links2 = soup2.select(".titleline > a")
subtext2 = soup2.select(".subtext")

all_links = links + links2
all_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k:k["votes"], reverse=True)

def add_hn_to_textfile(hn):
    with open("hn_votes.txt", "w") as file:
        for item in hn:
            file.write(f"{item["title"]}\n")
            file.write(f"{item["votes"]}\n")
            file.write(f"{item["link"]}\n")

def create_custom_hn(links, subtext):
    hn =[]
    for index, item in enumerate(links):
        title = item.get_text()
        href = item.get('href', None)
        vote = subtext[index].select(".score")
        if len(vote):
           points = int(vote[0].get_text().replace(" points", ""))
           if points >= 100:
             hn.append({'title': title, 'link': href, "votes": points})
    add_hn_to_textfile(hn)
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(all_links, all_subtext))