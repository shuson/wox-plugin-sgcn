# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://bbs.sgcn.com/forum.php?mod=forumdisplay&fid=197&filter=author&orderby=dateline'
URL2 = 'http://bbs.sgcn.com/forum.php?mod=forumdisplay&fid=160&filter=author&orderby=dateline'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):
  
    def request(self,url):
	#get system proxy if exists
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
	    proxies = {
		"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
		"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
	    }
	    return requests.get(url,proxies = proxies)
	return requests.get(url)
			
    def query(self, param):
        url = URL
        if param.strip() == 'phone':
            url = URL2
        
	r = self.request(url)
	r.encoding = 'utf-8'
	bs = BeautifulSoup(r.content, 'html.parser')
	posts = bs.select('tbody[id^=normalthread]')

	result = []
	for p in posts:
            ptitle = p.find('a', class_='s xst')
            ptime = p.find('span').string
            pname = p.find('cite').find('a').string
            item = {
                'Title': u'{subject}'.format(subject=full2half(ptitle.string)),
                'SubTitle': u'by: {name} | {time}'.format(name=pname, time=ptime),
                'IcoPath': os.path.join('img', 'sgcn.png'),
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [ptitle['href']]
                }
            }
            result.append(item)
        
	return result
    
    def open_url(self, url):
	webbrowser.open(url)

if __name__ == '__main__':
    Main()
