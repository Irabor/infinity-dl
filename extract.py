#!/usr/bin/env python
import re
import os
import sys
import string
import urllib2
import time
from urlparse import urlparse
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
headers_ = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": user_agent,
    "Connection": "keep-alive",
}
class Extractor(object):
    def __inti__(self, url, html):
        self.url = url
        self.html = html
    def send_request(self):
        self.url = sys.argv[1]
        print('Sending request...\n')
        time.sleep(3)
        print('Getting thread...')
        self.html = urllib2.Request(self.url, headers=headers_)
        self.html = urllib2.urlopen(self.html)
        self.html = self.html.read()
        return self.html
    def get_title(self):
        self.html = self.send_request()
        match = re.search(r'\<title\>(.+?)\<', self.html)
        if match:
            title = match.group()
            title = title.replace('<title>','').replace('<','')
            print('Thread title: '+title)
            return self.html
        else:
            print('Title not found')
    def strip_tags(self, tag): #THIS STRIP THE TAGS
        tag_frag = ['</a','<a','>','"','\'','href','=','//',' ','<','https', 'http://',':']
        for i in tag_frag:
            tag = tag.replace(i,'')
        return tag
    def parse_html(self, links):
        for match in links:
            links = match.group()
            links = self.strip_tags(links)
            urlp = urlparse(links)
            argurlp = urlparse(self.url)
            if 'endchan' in self.url:
                links = argurlp.scheme+'://'+argurlp.netloc+links
            if urlp.scheme == '':
                links = argurlp.scheme+'://'+links
            print links
            '''filenames = links.split('/')[-1]
            get_files = urllib2.Request(links, headers=headers_)
            get_files = urllib2.urlopen(get_files)
            get_files = get_files.read()
            with open(filenames, 'wb')as f:
                f.write(get_files)
                print('Downloading '+ filenames)'''
ext= Extractor()
ext.get_title()
ext_ = Extractor()
def _8ch_parser():
    file_urls = re.compile(r'(\<a\shref\=\"https\:\/\/\w+\d\.\d\w+\.\w+\/\w{1,10}\/\w{3}\/\d+(.)?(\d+)?\.(png|jpg|gif|webm|mp4|pdf)\"\s)')
    file_urls = re.finditer(file_urls, ext.html)
    ext.parse_html(file_urls)
def _4chan_parser():
    file_urls = re.compile(r'(\<a\s\w+\=\"\/\/\w{1}\.\d\w+\.\w+\/\w{1,4}\/\d+\.(png|jpg|webm|jpeg|gif|pdf))')
    file_urls = re.finditer(file_urls,ext.html)
    ext.parse_html(file_urls)
def _7chan_parser():
    file_urls = re.compile(r'(\<a\s\w+\=\"\w+\:\/\/\d\w+\.\w+\/(\w{1,5}|\d{1,5})\/\w{3}\/\d+\.(png|jpg|pdf|webm|gif))')
    file_urls = re.finditer(file_urls, ext.html)
    ext.parse_html(file_urls)
def _end_chan():
    file_urls =  re.compile(r'(\/\.\w{5}\S+alias\S+(png|jpg|webm|jpeg|gif)\")')
    file_urls = re.finditer(file_urls, ext.html)
    ext.parse_html(file_urls)
funclist = [_8ch_parser,_4chan_parser, _7chan_parser, _end_chan]
def main():
    for func in funclist:
        func()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as key:
        print('Download interrupted: %s' %(key))
    except urllib2.HTTPError as httperror:
        print 'Download iterrupted: %s' %(httperror)
