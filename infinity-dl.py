#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys, shutil, requests, time, os
argv = sys.argv
infin = "8ch.net"
_7ch = "7chan.org"
server_err = [404, 401, 500, 403, 400]
def _err_(err):
	sys.stderr.write(err)
def progress(pro):
	sys.stdout.write(pro)
	sys.stdout.flush()
	time.sleep(1)
def _7ch_scraper():
	get_url = requests.get(argv[1], verify=True)
	for errors in server_err:
		if get_url.status_code == errors:
			_err_(str(get_url.status_code)  + " Error\n")
			sys.exit()
	parse_html = BeautifulSoup(get_url.text, "lxml")
	for p_tags in parse_html.find_all("p", {"class": "file_size"}):
		for a_tags in p_tags.find_all("a"):
			url = a_tags.get("href")
			for the_url in a_tags:
				file_names = []
				file_names.append(the_url.split("/")[-1])
				for names in file_names:
					filenames = names
					get_files = requests.get(url, stream=True, verify=True)
					progress("Downloading " + filenames + " ......\n")
					with open(filenames, "wb")as outfile:
						shutil.copyfileobj(get_files.raw, outfile)
					del get_files
def _8ch_scraper():
		url = requests.get(argv[1], verify=True)
		for errors in server_err:
			if url.status_code == errors:
				_err_(str(url.status_code) + " Error\n")
				sys.exit()
		soup = BeautifulSoup(url.text, "lxml")
		for tags in soup.find_all("div", {"class" : "file"}):
			for span in tags.find_all("p", {"class" : "fileinfo"}):
				for post_file_name  in span.find_all("span", {"class": "postfilename"}):
					filenames = post_file_name.get_text()
				for a_tags in span.find_all("a"):
					media_list = a_tags.get("href")
					r = requests.get(media_list, stream=True, verify=True)
					progress("Downloading " + filenames + " ......\n")
					with open(filenames, "wb") as out_file:
						shutil.copyfileobj(r.raw, out_file)
					del r
def main():
	if len(argv) > 2 :
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()
	elif len(argv) < 2 :
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()
	if infin in argv[1]:
		progress("\033[32m\033[5mSending request...\n")
		progress("\033[0m\033[0m \n")
		progress("  \n")
		_8ch_scraper()
	if _7ch in argv[1]:
			progress("\033[32m\033[5mSending request...\n")
			progress("\033[0m\033[0m \n")
			progress("  \n")
			_7ch_scraper()
if __name__ == "__main__":
	main()
