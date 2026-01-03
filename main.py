from bs4 import BeautifulSoup
from lxml import etree
from collections import deque
import requests

def main():
    print(parse("https://en.wikipedia.org/wiki/Measure_(mathematics)"))

def parse(url):

    # Set headers to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    # Fetch the page
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    # Convert to etree for XPath
    dom = etree.HTML(str(soup))

    # Extract links using XPath
    links = dom.xpath('//p/a/@href')
    return links

def bfs():
    queue = deque()
    

if __name__ == "__main__":
    main()
