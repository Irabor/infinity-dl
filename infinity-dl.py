#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys, shutil, requests, time
def _err_(err):
	sys.stderr.write(err)
def progress(pro):
	sys.stdout.write(pro)
	sys.stdout.flush()
	time.sleep(1)
	
def main():
	argv = sys.argv
	infin = "8ch.net"
	if len(argv) > 2 :
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()
	elif len(argv) < 2 :
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()
	if infin in argv[1]:
		pass
	else:
		print("Invalid [URL]")
		_err_("Usage: " + argv[0] + " [URL]\n")
		sys.exit()
	url = requests.get(argv[1])
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
if __name__ == "__main__":
	main()
