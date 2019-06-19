# This page deals with summarisation of the description.

import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize
import random


def get_summary_description(link, token):
    text = get_text_from_link(link)
    if token == 'fb':
        x = random.randint(35, 120)
    if token == 'tw':
        x = random.randint(25, 31)
    desc = summarize(text, word_count=x)
    return desc


def get_text_from_link(link):
    link.strip()
    # Path to extract details from. This should be the input to this function.
    path = link

    # Extracting information.
    page = requests.get(path)
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)
    html = list(soup.children)[2]
    list(html.children)
    body = list(html.children)[3]
    #para = list(body.children)[1]

    # print(para.get_text())
    texti = soup.find_all('p')
    matter = ''

    count_of_paragraphs = 0
    for x in texti:
        matter = matter + x.get_text()
        count_of_paragraphs = count_of_paragraphs + 1
        if count_of_paragraphs > 1:
            return matter

    return matter
