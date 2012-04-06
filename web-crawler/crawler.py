#Finish crawl web
import urllib

def get_page(url):
    try:
	return urllib.urlopen(url).read()
    except:
	return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q,depth):
    for e in q:
        if e not in p:
            p.append([e,depth+1])

def add_to_index(index,keyword,url):
    if keyword in index:
	index[keyword].append(url)
    else:
	index[keyword] = [url]

def add_page_to_index(index,url,content):
    keywords = content.split()
    for keyword in keywords:
        add_to_index(index,keyword,url)

def lookup(index,keyword):
    if keyword in index:
	return index[keyword]
    return None

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed,maxdepth):
    tocrawl = [[seed,0]]
    crawled = []
    index = {}
    while tocrawl:
        page,depth = tocrawl.pop()
        if page not in crawled and depth <= maxdepth:
            crawled.append(page)
	    content = get_page(page)
	    add_page_to_index(index,page,content)
            union(tocrawl,get_all_links(content),depth)
    return index

print crawl_web('http://www.google.com',0)
