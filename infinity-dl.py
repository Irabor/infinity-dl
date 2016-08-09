#!/usr/bin/env python
#Copyright (c) 2016 Irabor

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#This script scraps media files from imageboard threads

from __future__ import division
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
        print('[HTTP error]: %s \n Check your url' %e.reason)
        sys.exit()
    else:
        page = urllib2.urlopen(r)
        webpage = page.read()
        return webpage
def write_file(fh,fn):
    with open(sys.argv[2]+fn ,'wb')as f:
        f.write(fh)
def calc_size(size):
    if size > 1024:
        size = size /1024
        ch = size % 2
        if ch == 0:
            size = "%d MB"%(size)
            return size
        else:
            size = "%1.2f MB"%(size)
            size = str(size)
            return size
    else:
        size = '%d KB'%(size)
        return size
def tfs(size):
    size = size / 1024
    if size > 1024:
        size = size /1024
        ch = size % 2
        if ch == 0:
            size = '%d MB'%(size)
            return size
        else:
            size = '%1.2f MB'%(size)
            return size
    else:
        size = '%d KB'%(size)
        return size
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
    total_size = ''
    sf = 0
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
        elif not url.scheme and ('//' in i) and (not url.query):
            file_links.append(lu.scheme+':'+i)
        else:
            if '//' not in i and (not url.query):
                file_links.append(base+i)
    #print file_links
    print("Media list: %d" %(len(file_links)))
    for ln in file_links:
        file_ = re_page(ln)
        fs = len(file_) / 1024
        sf += len(file_)
        fs = calc_size(fs)
        filenames = ln.split('/')[-1]
        write_file(file_,filenames)
        counter+= 1
        print("[Downloading] %s %d / %d - %s"%(filenames, counter, len(file_links),fs))
    total_size = tfs(sf)
    print('[Finished] Total size: %s'%(total_size))
if __name__ == '__main__':
    try:
       parse_html()
    except KeyboardInterrupt:
        print('\n[Abortion] Download aborted')
        sys.exit()
    except IndexError:
        print('Usage: %s [URL] [DIR]'%(sys.argv[0]))
