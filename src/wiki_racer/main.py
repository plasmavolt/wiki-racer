from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from lxml import etree
from collections import deque
import requests
from link import Link

def main():
    # start = input("starting url: ")
    # end = input("ending url: ")
    start = "https://en.wikipedia.org/wiki/Measure_(mathematics)"
    end = "https://en.wikipedia.org/wiki/List_of_geometers"
    Link = bfs(start, end)
    print(Link)

def parse(url: str) -> list:
    """
    Parses a wiki page for links to other wiki pages.

    Args:
        url (str): the url to be parsed

    Returns:
        list: all links in body of wiki page
    """

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

def bfs(start: str, end: str) -> Optional[Link]:
    """
    Performs BFS starting at a given wiki page and ending at another.

    Args:
        start (str): the starting wiki page
        end (str): the desired ending wiki page

    Returns:
        Link: a Link object with the shortest Link found
    """
    queue = deque() # stores Link objects
    seen = set() # stores url strings
    
    queue.append(Link(start, [start]))
    while len(queue) > 0:
        curr = queue.popleft()
        print(curr)
        if curr.url in seen:
            continue
        seen.add(curr.url)
        
        if curr.url == end:
            return curr
        
        for link in parse(curr.url):
            if link not in seen:
                full_link = 'https://' + urlparse(curr.url).netloc + link
                new_path = curr.path[:]
                new_path.append(full_link)
                queue.append(Link(full_link, new_path))

if __name__ == "__main__":
    main()
