#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys, shutil, requests, time
argv = sys.argv
infin = "8ch.net"
_7ch = "7chan.org"
def _err_(err):
	sys.stderr.write(err)
def progress(pro):
	sys.stdout.write(pro)
	sys.stdout.flush()
	time.sleep(1)
def _7ch_scraper():
	get_url = requests.get(argv[1], verify=True)
	parse_html = BeautifulSoup(get_url.text, "lxml")
	progress("Downloading... \n")
	for p_tags in parse_html.find_all("p", {"class": "file_size"}):
		for a_tags in p_tags.find_all("a"):
			url = a_tags.get("href")
			for the_url in a_tags:
				file_names = []
				file_names.append(the_url.split("/")[-1])
				for names in file_names:
					filenames = names
					get_files = requests.get(url, stream=True, verify=True)
					with open(filenames, "wb")as outfile:
						shutil.copyfileobj(get_files.raw, outfile)
					del get_files
def _8ch_scraper():
		url = requests.get(argv[1], verify=True)
		soup = BeautifulSoup(url.text, "lxml")
		progress("Downloading... \n")
		for tags in soup.find_all("div", {"class" : "file"}):
			for span in tags.find_all("p", {"class" : "fileinfo"}):
				for post_file_name  in span.find_all("span", {"class": "postfilename"}):
					filenames = post_file_name.get_text()
				for a_tags in span.find_all("a"):
					media_list = a_tags.get("href")
					r = requests.get(media_list, stream=True, verify=True)
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
		_8ch_scraper()
	if _7ch in argv[1]:
		_7ch_scraper()
	else:
		print("Invalid [URL]")
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()

if __name__ == "__main__":
	main()
