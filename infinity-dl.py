#!/usr/bin/env python
from HTMLParser import HTMLParser as hp
import sys
import urllib2
from urlparse import urlparse
import requests
class Parser(hp):
    def __init__(self):
        hp.__init__(self)
        self.links =[]
    def handle_starttag(self,tag,attrs):
        for name, value in attrs:
            if name == 'href':
                self.links.append(value)
if len(sys.argv) == 3:
    print('Sending request..')
def re_page(url):
    ua = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    r = urllib2.Request(url, headers = ua)
    try:
        page = urllib2.urlopen(r)
    except urllib2.HTTPError,e:
        print('[HTTP error]: %s ' %e.reason)
        sys.exit()
    else:
        page = urllib2.urlopen(r)
        webpage = page.read()
        return webpage
def write_file(fh,fn):
    with open(sys.argv[2]+fn ,'wb')as f:
        f.write(fh)
def parse_html():
    page = re_page(sys.argv[1])
    pg = Parser()
    pg.feed(page)
    links = pg.links
    fe = ['.png','.jpg','.webm','.gif','.mp4','.jpeg']
    unsorted_links =[]
    media_links = []
    file_links = []
    al = []
    counter = 0
    lu = urlparse(sys.argv[1])
    base = "%s://%s"%(lu.scheme, lu.netloc)
    for i in links:
        for n in fe:
            if n in i:
                unsorted_links.append(i)
    for l in unsorted_links:
        if l not in media_links:
            media_links.append(l)
    for i in media_links:
        url = urlparse(i)
        if url.scheme and (not url.query):
            file_links.append(i)
        elif not url.scheme and ('//' in i):
            file_links.append(lu.scheme+':'+i)
        else:
            if '//' not in i and (not url.query):
                file_links.append(base+i)
    #print file_links
    print("File list: %d" %(len(file_links)))
    for ln in file_links:
        file_ = re_page(ln)
        filenames = ln.split('/')[-1]
        write_file(file_,filenames)
        counter+= 1
        print("Downloading %s... [%d / %d]"%(filenames, counter, len(file_links)))
if __name__ == '__main__':
    try:
        parse_html()
    except KeyboardInterrupt:
        sys.exit()
    except IndexError:
        print('Usage: %s [URL]'%(sys.argv[0]))
