#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys, shutil, requests, time, os

argv = sys.argv
infin = "8ch.net"
_7ch = "7chan.org"
_4chan = '4chan.org'
hispanchan_url = 'hispachan.org'
server_err = [404, 401, 500, 502, 403, 400]
def _err_():
	sys.stderr.write("Usage: " + argv[0] + " [URL] [DIR]\n")
def send_request():
	sys.stdout.write("\n")
	sys.stdout.flush()
	sys.stdout.write("\033[32m\033[5mSending request...\n")
	sys.stdout.flush()
	sys.stdout.write("\033[0m\033[0m \n")
	sys.stdout.flush()
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
					print("Downloading " + filenames)
					with open(filenames, "wb")as outfile:
						shutil.copyfileobj(get_files.raw, outfile)
						shutil.move(filenames, argv[2])
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
					print("Downloading " + filenames)
					with open(filenames, "wb") as out_file:
						shutil.copyfileobj(r.raw, out_file)
						shutil.move(filenames, argv[2])
					del r
def _4chan_scraper():
	url = requests.get(argv[1], verify=True)
	for errors in server_err:
		if url.status_code == errors:
			_err_(str(url.status_code) + " Error\n")
			sys.exit()
	parse_html = BeautifulSoup(url.text, "lxml")
	for tags in parse_html.find_all("div", {"class": "fileText"}):
		for a_tags in tags.find_all("a"):
			usplit_link = a_tags.get("href")
			media_list_url = "https://" + usplit_link.split("//")[-1]
			filenames = a_tags.get_text()
			get_files = requests.get(media_list_url, stream= True, verify=True)
			print("Downloading "+ filenames)
			print(".......................................")
			with open(filenames, "wb")as outfile:
				shutil.copyfileobj(get_files.raw, outfile)
				shutil.move(filenames, argv[2])
			del get_files
def hispanchan():
		url = requests.get(argv[1], verify=True)
		for errors in server_err:
			if url.status_code == errors:
				_err_(str(url.status_code) + " Error\n")
				sys.exit()
		parse_html = BeautifulSoup(url.text, "lxml")
		for span in parse_html.find_all('span',{'class' : 'filenamereply'}):
			for a_tags in span.find_all('a'):
				filenames = a_tags.get('href').split('/')[-1]
				media_list_url = a_tags.get('href')
				get_files = requests.get(media_list_url, stream=True, verify=True)
				print("Downloading "+ filenames)
				print(".......................................\n")
				with open(filenames, 'wb')as outfile:
					shutil.copyfileobj(get_files.raw, outfile)
					shutil.move(filenames, argv[2])
def main():
	if (len(argv) > 3) and (os.path.isdir(argv[2]) == False):
		_err_()
		sys.exit()
	elif (len(argv) < 3) or (os.path.isdir(argv[2]) == False):
		_err_()
		sys.exit()
	if infin in argv[1]:
		send_request()
		_8ch_scraper()
	if _7ch in argv[1]:
		send_request()
		_7ch_scraper()
	if _4chan in argv[1]:
		send_request()
		_4chan_scraper()
	if hispanchan_url in argv[1]:
		send_request()
		hispanchan()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt or IndexError:
		print("  \n")
		print("\033[31mDownload interrupted\n")
		sys.exit()
