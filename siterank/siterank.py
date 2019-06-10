#!/usr/bin/env python3
##
# Script to fetch alexa ranks for one or more websites.
# Usage: siterank <url1> <url2> ....
#
# @author Prahlad Yeri
#
import urllib.request
import sys, os
import xml.etree.ElementTree as ET

def main():
	if len(sys.argv) == 1:
		print("Insufficient parameters.")
		exit()
	urls = sys.argv[1:]
	ranks = {}
	for url in urls:
		#https://stackoverflow.com/questions/3676376/fetching-alexa-data
		turl = "http://data.alexa.com/data?cli=10&url=" + url
		req = urllib.request.Request(turl)
		with urllib.request.urlopen(req) as fp:
			output = fp.read().decode('utf-8')
			tree = ET.ElementTree(ET.fromstring(output))
			root = tree.getroot()
			sd = root.find("SD")
			if sd != None:
				rnk = int(sd.find("POPULARITY").get("TEXT"))
				ranks[url] = rnk
			else:
				print("Not found: " + url)
	sranks = [(k,ranks[k]) for k in sorted(ranks, key=ranks.get, reverse=False)]
	for k,v in sranks:
		rank = v
		if rank > 1000:
			rank = str(int(rank/1000)) + "K"
		print(k, rank)

if __name__ == "__main__":
	main()
